import json
from datetime import date, datetime

from django.contrib.postgres.search import TrigramSimilarity
from django.core.cache import cache
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView

from .forms import SearchForm
from .models import MultipleChoiceQuestion, MultipleChoiceSubmission, Olympiad, OlympiadUser, OneChoiceQuestion, \
    OneChoiceSubmission, Subject, TrueFalseQuestion, TrueFalseSubmission
from ..courses.models import Course
from ..students.models import User


def index(request):
    courses = Course.objects.annotate(participant_count=Count('participants')) \
        .select_related('teacher') \
        .order_by('-participant_count')[:6]
    olympiads = Olympiad.objects.annotate(participant_count=Count('participants')).order_by('-participant_count')[:3]
    context = {
        'courses': courses,
        'olympiads': olympiads
    }
    return render(request, 'olympiads/index.html', context)


def is_not_ready(request):
    return render(request, 'is_not_ready.html')


class UserOlympiadList(ListView):
    model = Olympiad
    template_name = 'olympiads/olympiads_list.html'
    ordering = '-date_of_start'
    context_object_name = 'olympiads'

    def get_queryset(self):
        queryset = self.request.user.olympiad_set.select_related('subject').all()
        search_word = self.request.GET.get('keyword')

        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        student = self.request.user
        user_submissions = OlympiadUser.objects.filter(user=student)
        context['user_submissions'] = user_submissions
        return context


class UserPreviousOlympiadList(UserOlympiadList):
    def get_queryset(self):
        queryset = self.request.user.olympiad_set.select_related('subject').all().filter(date_of_start__lt=date.today())
        search_word = self.request.GET.get('keyword')

        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset


class UserComingOlympiadList(UserOlympiadList):
    def get_queryset(self):
        queryset = self.request.user.olympiad_set.select_related('subject').all().filter(date_of_start__gt=date.today())
        search_word = self.request.GET.get('keyword')

        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset


class OlympiadList(ListView):
    model = Olympiad
    template_name = 'olympiads/all_olympiads.html'
    context_object_name = 'olympiads'

    def get_queryset(self):
        queryset = Olympiad.objects.all().select_related('subject').filter(date_of_start__gt=date.today())
        search_word = self.request.GET.get('keyword', None)
        stage = self.request.GET.get('stage', None)
        subject = self.request.GET.get('subject', None)

        if search_word:
            queryset = (Olympiad.objects.annotate(similarity=TrigramSimilarity('title', search_word))
                        .filter(similarity__gt=0.1, date_of_start__gt=date.today())
                        .select_related('subject')
                        .order_by('-similarity'))
            return queryset

        if stage:
            key_stage = f'olympiad_stage{stage}'
            cached_queryset = cache.get(key_stage)
            if not cached_queryset:
                cached_queryset = queryset.filter(stage__exact=stage)
                cache.set(key_stage, cached_queryset)
            return cached_queryset

        if subject:
            key_subject = f'olympiad_subject{subject}'
            cached_queryset = cache.get(key_subject)
            if not cached_queryset:
                cached_queryset = queryset.filter(subject__exact=subject)
                cache.set(key_subject, cached_queryset)
            return cached_queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        subjects = cache.get('subjects')
        if not subjects:
            subjects = Subject.objects.all()
            cache.set('subjects', subjects)
        context['subjects'] = subjects

        stages = cache.get('stages')
        if not stages:
            stages = set(Olympiad.objects.values_list('stage', flat=True))
            cache.set('stages', stages)
        context['stages'] = stages
        return context


def olympiad_page(request, olympiad_id):
    olympiad = Olympiad.objects.get(id=olympiad_id)
    student = User.objects.get(id=request.user.id)
    key = f'olympiad_page{olympiad.id}'
    context = cache.get(key)
    if not context:
        try:
            o_questions = OneChoiceQuestion.objects.filter(olympiad=olympiad)
        except OneChoiceQuestion.DoesNotExist:
            o_questions = None

        try:
            m_questions = MultipleChoiceQuestion.objects.filter(olympiad=olympiad)
        except MultipleChoiceQuestion.DoesNotExist:
            m_questions = None

        try:
            t_questions = TrueFalseQuestion.objects.filter(olympiad=olympiad)
        except TrueFalseQuestion.DoesNotExist:
            t_questions = None

        context = {
            'olympiad': olympiad,
            'o_questions': o_questions,
            'm_questions': m_questions,
            't_questions': t_questions
        }
        cache.set(key, context)

    try:
        submission = OlympiadUser.objects.get(user=student, olympiad=olympiad)
    except OlympiadUser.DoesNotExist:
        submission = OlympiadUser.objects.create(user=student, olympiad=olympiad)

    try:
        o_submissions = OneChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    except OneChoiceSubmission.DoesNotExist:
        o_submissions = None

    try:
        m_submissions = MultipleChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    except MultipleChoiceSubmission.DoesNotExist:
        m_submissions = None

    try:
        t_submissions = TrueFalseSubmission.objects.filter(student=student, question__olympiad=olympiad)
    except TrueFalseSubmission.DoesNotExist:
        t_submissions = None

    extra_context = {
            'student': student,
            'o_submissions': o_submissions,
            'm_submissions': m_submissions,
            't_submissions': t_submissions,
        }
    context.update(extra_context)
    if not submission.is_finished:
        return render(request, 'olympiads/olympiad_page.html', context)

    else:
        all_submissions = (OlympiadUser.objects.filter(olympiad=olympiad)
                           .select_related('user').order_by('ranking_place'))
        context.update({
            'submission': submission,
            'all_submissions': all_submissions
        })
        return render(request, 'olympiads/olympiad_page_results.html', context)


def submit_o_question_answer(request):
    if request.method == 'POST':
        student = request.user
        try:
            data = json.loads(request.body)
            olympiad_id = data.get('olympiad_id')
            question_id = data.get('question_id')
            answer = data.get('answer')

            try:
                olympiad = Olympiad.objects.get(id=olympiad_id)
                question = OneChoiceQuestion.objects.get(id=question_id, olympiad=olympiad)
            except OneChoiceQuestion.DoesNotExist:
                response_data = {
                                 'status': 'error',
                                 'message': 'вопрос не найден'
                }
                return JsonResponse(response_data, status=400)

            try:
                submission = OneChoiceSubmission.objects.get(question=question, student=student)
            except OneChoiceSubmission.DoesNotExist:
                submission = OneChoiceSubmission.objects.create(student=student, question=question)

            submission.a = submission.b = submission.c = submission.d = False
            submission.save()

            if answer in ['A', 'B', 'C', 'D']:
                setattr(submission, answer.lower(), True)
                submission.save()

            if question.a_is_correct == submission.a and question.b_is_correct == submission.b and \
               question.c_is_correct == submission.c and question.d_is_correct == submission.d:
                submission.students_mark = question.mark
            else:
                submission.students_mark = 0
            submission.save()

            response_data = {
                'status': 'success',
                'message': 'Данные успешно обработаны.'
                }
            return JsonResponse(response_data)

        except Exception:
            response_data = {
                'status': 'error',
                'message': 'Ошибка при разборе данных JSON.'
            }
            return JsonResponse(response_data, status=400)


def submit_t_question_answer(request):
    if request.method == 'POST':
        student = request.user
        try:
            data = json.loads(request.body)
            olympiad_id = data.get('olympiad_id')
            question_id = data.get('question_id')
            answer = data.get('answer')

            try:
                olympiad = Olympiad.objects.get(id=olympiad_id)
                t_question = TrueFalseQuestion.objects.get(id=question_id, olympiad=olympiad)
            except TrueFalseQuestion.DoesNotExist:
                response_data = {
                                 'status': 'error',
                                 'message': 'вопрос не найден'
                }
                return JsonResponse(response_data, status=400)

            try:
                submission = TrueFalseSubmission.objects.get(student=student, question=t_question)
            except TrueFalseSubmission.DoesNotExist:
                submission = TrueFalseSubmission.objects.create(student=student, question=t_question)

            submission.answer = answer
            submission.save()

            if submission.answer == t_question.answer:
                submission.students_mark = t_question.mark
            else:
                submission.students_mark = 0
            submission.save()

            response_data = {
                    'status': 'success',
                    'message': 'Данные успешно обработаны.'
                    }
            return JsonResponse(response_data)

        except Exception:
            response_data = {
                'status': 'error',
                'message': 'Ошибка при разборе данных JSON'
            }
            return JsonResponse(response_data, status=400)


def submit_olympiad_answer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        olympiad_id = data.get('olympiad_id')
        olympiad = Olympiad.objects.get(id=olympiad_id)
        student_id = data.get('student_id')
        student = User.objects.get(id=student_id)
        multipleanswers = data.get('user_answers')

        for id_question in multipleanswers:
            if id_question:
                try:
                    question = MultipleChoiceQuestion.objects.get(id=id_question, olympiad__id=olympiad_id)
                except MultipleChoiceQuestion.DoesNotExist:
                    response_data = {
                                    'status': 'error',
                                    'message': 'Ошибка при разборе данных JSON.'
                    }
                    return JsonResponse(response_data, status=400)

                try:
                    question_submission = MultipleChoiceSubmission.objects.get(question=question, student=student)
                except MultipleChoiceSubmission.DoesNotExist:
                    question_submission = MultipleChoiceSubmission.objects.create(student=student, question=question)

                for answer in multipleanswers[id_question]:
                    if answer in ['A', 'B', 'C', 'D', 'E', 'F']:
                        setattr(question_submission, answer.lower(), True)
                question_submission.save()

                total = 6
                correct = 0
                if question_submission.a == question_submission.question.a_is_correct:
                    correct += 1
                if question_submission.b == question_submission.question.b_is_correct:
                    correct += 1
                if question_submission.c == question_submission.question.c_is_correct:
                    correct += 1
                if question_submission.d == question_submission.question.d_is_correct:
                    correct += 1
                if question_submission.e == question_submission.question.e_is_correct:
                    correct += 1
                if question_submission.f == question_submission.question.f_is_correct:
                    correct += 1

                if total == correct:
                    question_submission.students_mark = question.mark
                else:
                    question_submission.students_mark = 0
                question_submission.save()

        try:
            submission = OlympiadUser.objects.get(olympiad=olympiad, user=student)
        except OlympiadUser.DoesNotExist:
            submission = OlympiadUser.objects.create(user=student, olympiad=olympiad)

        submission.is_finished = True
        submission.save()

        compute_score(student, olympiad, submission)
        update_olympiad_user_ranking(olympiad)
        response_data = {
                         'status': 'success',
                         'message': 'Данные успешно обработаны'
            }
        return JsonResponse(response_data)


def compute_score(student, olympiad, submission):
    submission.earned_mark = 0

    o_submissions = OneChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    for o_submission in o_submissions:
        submission.earned_mark += o_submission.students_mark

    m_submissions = MultipleChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    for m_submission in m_submissions:
        submission.earned_mark += m_submission.students_mark

    t_submissions = TrueFalseSubmission.objects.filter(student=student, question__olympiad=olympiad)
    for t_submission in t_submissions:
        submission.earned_mark += t_submission.students_mark

    submission.save()


def update_olympiad_user_ranking(olympiad):
    olympiad_users = OlympiadUser.objects.filter(olympiad=olympiad, is_finished=True)
    for user in olympiad_users:
        earned_mark = user.earned_mark

        ranking_place = OlympiadUser.objects.filter(olympiad=olympiad, earned_mark__gt=earned_mark).count() + 1
        OlympiadUser.objects.filter(id=user.id).update(ranking_place=ranking_place)


def get_template_view(request):
    return render(request, 'olympiads/page_after_sending_olympiads_answers.html')


def olympiad_registration(request, olympiad_id):
    student = request.user
    olympiad = get_object_or_404(Olympiad, id=olympiad_id)
    result = olympiad.is_registrations_open()
    if olympiad not in student.olympiad_set.all():
        allow_register = True
        if result:
            OlympiadUser.objects.create(user=student, olympiad=olympiad, registration_date=datetime.now())
    else:
        allow_register = False

    context = {
            'olympiad': olympiad,
            'student': student,
            'result': result,
            'allow_register': allow_register
        }
    return render(request, 'olympiads/olympiad_main_page.html', context)
