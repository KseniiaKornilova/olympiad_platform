from datetime import date, datetime
import json
import os
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from ..students.models import User
from ..courses.models import OneChoiceQuestion, OneChoiceSubmission, MultipleChoiceQuestion, MultipleChoiceSubmission, TrueFalseQuestion, TrueFalseSubmission
from .models import Olympiad, Subject, OlympiadUser
from .forms import SearchForm


# Create your views here.

def index(request):
    return render(request, 'olympiads/index.html')


class UserOlympiadList(ListView):
    model = Olympiad
    template_name = 'olympiads/olympiads_list.html'
    ordering = '-date_of_start'
    context_object_name = 'olympiads'

    def get_queryset(self):
        queryset = self.request.user.olympiad_set.all()
        search_word = self.request.GET.get('keyword')

        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class UserPreviousOlympiadList(UserOlympiadList, ListView):
    def get_queryset(self):
        queryset = self.request.user.olympiad_set.all().filter(date_of_start__lt=date.today())
        search_word = self.request.GET.get('keyword')

        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset


class UserComingOlympiadList(UserOlympiadList, ListView):
    def get_queryset(self):
        queryset = self.request.user.olympiad_set.all().filter(date_of_start__gt=date.today())
        search_word = self.request.GET.get('keyword')

        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset


class OlympiadList(ListView):
    model = Olympiad
    template_name = 'olympiads/all_olympiads.html'
    context_object_name = 'olympiads'

    def get_queryset(self):
        queryset = Olympiad.objects.all().filter(date_of_start__gt=date.today())
        search_word = self.request.GET.get('keyword', None)
        stage = self.request.GET.get('stage', None)
        subject = self.request.GET.get('subject', None)

        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        if stage:
            queryset = queryset.filter(stage__exact=stage)
        if subject:
            queryset = queryset.filter(subject__exact=subject)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        context['subjects'] = Subject.objects.all()
        context['stages'] = Olympiad.objects.values_list('stage', flat=True).distinct()
        return context


def olympiad_page(request, olympiad_id, user_id):
    olympiad = Olympiad.objects.get(id=olympiad_id)
    student = User.objects.get(id=user_id)
    try:
        submission = OlympiadUser.objects.get(user=student, olympiad=olympiad)
    except OlympiadUser.DoesNotExist:
        submission = OlympiadUser.objects.create(user=student, olympiad=olympiad)

    try:
        o_questions = OneChoiceQuestion.objects.filter(olympiad=olympiad)
    except OneChoiceQuestion.DoesNotExist:
        o_questions = None
    try:
        o_submissions = OneChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    except OneChoiceSubmission.DoesNotExist:
        o_submissions = None

    try:
        m_questions = MultipleChoiceQuestion.objects.filter(olympiad=olympiad)
    except MultipleChoiceQuestion.DoesNotExist:
        m_questions = None
    try:
        m_submissions = MultipleChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    except MultipleChoiceSubmission.DoesNotExist:
        m_submissions = None

    try:
        t_questions = TrueFalseQuestion.objects.filter(olympiad=olympiad)
    except TrueFalseQuestion.DoesNotExist:
        t_questions = None
    try:
        t_submissions = TrueFalseSubmission.objects.filter(student=student, question__olympiad=olympiad)
    except TrueFalseSubmission.DoesNotExist:
        t_submissions = None
    
    if not submission.is_finished:
        context = {
            'olympiad': olympiad, 
            'student': student,
            'o_questions': o_questions,
            'o_submissions': o_submissions,
            'm_questions': m_questions,
            'm_submissions': m_submissions,
            't_questions': t_questions,
            't_submissions': t_submissions
        }

        return render(request, 'olympiads/olympiad_page.html', context)

    else:
        all_submissions = OlympiadUser.objects.filter(olympiad=olympiad)
        result_context = {
            'olympiad': olympiad, 
            'student': student,
            'o_questions': o_questions,
            'o_submissions': o_submissions,
            'm_questions': m_questions,
            'm_submissions': m_submissions,
            't_questions': t_questions,
            't_submissions': t_submissions,
            'submission': submission,
            'all_submissions': all_submissions
        }
        return render(request, 'olympiads/olympiad_page_results.html', result_context)


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
                'message': 'Ошибка при разборе данных JSON.'
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

            if question.a_is_correct == submission.a and question.b_is_correct == submission.b and question.c_is_correct == submission.c and question.d_is_correct == submission.d:
                submission.students_mark = question.mark
            else:
                submission.students_mark = 0
            submission.save()

            response_data = {
                'status': 'success',
                'message': 'Данные успешно обработаны.'
                }
            return JsonResponse(response_data)

        except:
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
                'message': 'ошибка в нахождении олимпиады и вопроса'
                }
                return JsonResponse(response_data, status=400)

            try:
                submission = TrueFalseSubmission.objects.get(student=student, question=t_question)
            except TrueFalseSubmission.DoesNotExist:
                submission = TrueFalseSubmission.objects.create(student=student, question=t_question)

            submission.answer = answer
            submission.save()

            if submission.answer == t_question.answer:
                submission.students_mark = t_question.marks
            else:
                submission.students_mark = 0
            submission.save()

            response_data = {
                    'status': 'success',
                    'message': 'Данные успешно обработаны.'
                    }
            return JsonResponse(response_data)

        except:
            response_data = {
                'status': 'error',
                'message': 'Ошибка при разборе данных JSON в конце.'
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
        response_data = {'status' : 'success', 'message' : 'submitted'}
        return JsonResponse(response_data)

def compute_score(student, olympiad, submission):
    submission.earned_mark = 0
    submission.total_mark = 0

    o_submissions = OneChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    for o_submission in o_submissions:
        submission.earned_mark += o_submission.students_mark
        submission.total_mark += o_submission.question.mark

    m_submissions = MultipleChoiceSubmission.objects.filter(student=student, question__olympiad=olympiad)
    for m_submission in m_submissions:
        submission.earned_mark += m_submission.students_mark
        submission.total_mark += m_submission.question.mark

    t_submissions = TrueFalseSubmission.objects.filter(student=student, question__olympiad=olympiad)
    for t_submission in t_submissions:
        submission.earned_mark += t_submission.students_mark
        submission.total_mark += t_submission.question.marks

    submission.save()


def update_olympiad_user_ranking(olympiad):
    olympiad_users = OlympiadUser.objects.filter(olympiad=olympiad, is_finished=True)
    for user in olympiad_users:
        earned_mark = user.earned_mark

        ranking_place = OlympiadUser.objects.filter(olympiad=olympiad, earned_mark__gt=earned_mark).count() + 1
        OlympiadUser.objects.filter(id=user.id).update(ranking_place=ranking_place)



def get_template_view(request):
    template_name = 'olympiads/page_after_sending_olympiads_answers.html'
    template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)

    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            html_template = file.read()
        return HttpResponse(html_template, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("Файл не найден", status=404)




def olympiad_registration(request, olympiad_id):
    student = request.user
    try:
        olympiad = Olympiad.objects.get(id=olympiad_id)
    except Olympiad.DoesNotExist:
        olympiad = None

    result = olympiad.is_registrations_open()
    if result:
        olympiad_user = OlympiadUser.create(user=student, olympiad=olympiad, registration_date=datetime.now())
    else:
        result = False
        olympiad_user = None

    context = {
            'olympiad': olympiad,
            'student': student,
            'result': result,
            'olympiad_user': olympiad_user
        }
    return render(request, 'olympiads/olympiad_main_page.html', context)