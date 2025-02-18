import json
from datetime import datetime

from django.contrib import messages
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.core.cache import cache
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView

from .forms import AssignmentSubmissionForm, AssignmentSubmissionTeacherCheckForm, UserCommentForm
from .models import Assignment, AssignmentSubmission, Comment, Course, CourseUser, Lesson
from ..olympiads.forms import SearchForm
from ..olympiads.models import Subject


class UserCoursesList(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        user = self.request.user
        if len(user.course_teacher.all()) == 0:
            queryset = user.course_participants.select_related('teacher').all()
        else:
            queryset = user.course_teacher.all()
        search_word = self.request.GET.get('keyword')
        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        if len(self.request.user.course_teacher.all()) == 0:
            context['status'] = 'student'
        else:
            context['status'] = 'teacher'
        return context


class CourseList(ListView):
    template_name = 'courses/all_courses.html'
    model = Course
    context_object_name = 'courses'

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        school_subject = self.request.GET.get('subject', None)
        search_word = self.request.GET.get('keyword')
        queryset = cache.get('all_courses')
        if not queryset:
            queryset = Course.objects.select_related('teacher').all()
            cache.set('all_courses', queryset)

        if category:
            key_category = f'courses_category_{category}'
            cached_queryset = cache.get(key_category)
            if not cached_queryset:
                cached_queryset = queryset.filter(category__exact=category)
                cache.set(key_category, cached_queryset)
            return cached_queryset

        if school_subject:
            key_subject = f'courses_subject_{school_subject}'
            cached_queryset = cache.get(key_subject)
            if not cached_queryset:
                cached_queryset = queryset.filter(subject__exact=school_subject)
                cache.set(key_subject, cached_queryset)
            return cached_queryset

        if search_word:
            queryset = Course.objects.annotate(similarity=TrigramSimilarity('title', search_word)
                                               ).filter(similarity__gt=0.1).order_by('-similarity')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['form'] = SearchForm(self.request.GET)

        student = self.request.user
        course_submissions = CourseUser.objects.select_related('course').filter(user=student)
        all_courses_id = list()
        for course_submission in course_submissions:
            all_courses_id.append(course_submission.course.id)
        context['all_courses_id'] = all_courses_id
        return context


def course_main_page(request, course_id):
    user = request.user
    key = f'course_main_page_{course_id}'
    context = cache.get(key)
    if not context:
        course = Course.objects.get(id=course_id)
        course_teacher = course.teacher

        try:
            assignments = Assignment.objects.filter(course=course).order_by('assignment_num')
        except Assignment.DoesNotExist:
            assignments = None

        try:
            lessons = Lesson.objects.filter(course=course).order_by('number')
        except Lesson.DoesNotExist:
            lessons = None

        context = {
            'course': course,
            'course_teacher': course_teacher,
            'assignments': assignments,
            'lessons': lessons
        }
        cache.set(key, context)
    course = context['course']

    if user != context['course_teacher']:
        try:
            course_submission = CourseUser.objects.get(user=user, course=course)
        except CourseUser.DoesNotExist:
            course_submission = CourseUser.objects.create(user=user, course=course)

        try:
            assignment_submissions = AssignmentSubmission.objects.select_related('assignment').filter(
                        student=user, assignment__course=course).order_by('assignment__assignment_num')
        except AssignmentSubmission.DoesNotExist:
            assignment_submissions = None

        assignment_submissions_done = AssignmentSubmission.objects.select_related('assignment').filter(
            assignment__course=course, student=user, is_finished=True)

        extra_context = {'student': user,
                         'course_submission': course_submission,
                         'assignment_submissions': assignment_submissions,
                         'assignment_submissions_done': assignment_submissions_done,
                         }
        student_context = {**context, **extra_context}
        return render(request, 'courses/course_main_page.html', student_context)

    else:
        course_students = course.participants.all().order_by('last_name')
        assignment_submissions_all = AssignmentSubmission.objects.filter(assignment__in=context['assignments'])

        extra_context = {
            'user': user,
            'course_students': course_students,
            'assignment_submissions_all': assignment_submissions_all,
        }
        teacher_context = {**context, **extra_context}
        return render(request, 'courses/course_main_page.html', teacher_context)


def lesson_view(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lessons = Lesson.objects.filter(course=course).order_by('number')
    search_word = request.GET.get('keyword')

    if search_word:
        form = SearchForm(request.GET)
        search_vector = SearchVector('title', 'content', config='russian')
        search_query = SearchQuery(search_word, config='russian')
        relevant_lessons = Lesson.objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')

    else:
        form = SearchForm()
        relevant_lessons = None

    context = {'course': course,
               'lesson': lesson,
               'lessons': lessons,
               'form': form,
               'relevant_lessons': relevant_lessons,
               'search_word': search_word
               }

    return render(request, 'courses/lesson_page.html', context)


def lesson_comment_view(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id)

    student = request.user
    created_at = datetime.now()
    initial = {'student': student, 'course': course, 'lesson': lesson, 'created_at': created_at}
    form = UserCommentForm(initial=initial)

    comments = Comment.objects.filter(lesson=lesson, course=course).order_by('-created_at')

    context = {'course': course,
               'lesson': lesson,
               'form': form,
               'comments': comments}

    return render(request, 'courses/lesson_page_comments.html', context)


def submit_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course_id = data.get('course_id')
            lesson_id = data.get('lesson_id')
            course = get_object_or_404(Course, id=course_id)
            lesson = get_object_or_404(Lesson, id=lesson_id)
            student = data.get('student')
            content = data.get('content')
            created_at = data.get('created_at')

            form_data = {'course': course,
                         'lesson': lesson,
                         'student': student,
                         'content': content,
                         'created_at': created_at}

            form = UserCommentForm(form_data)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
                return JsonResponse({'error': 'Неверные данные'})

            comments = Comment.objects.filter(course=course, lesson=lesson).order_by('-created_at').values()
            return JsonResponse(list(comments), safe=False)

        except json.JSONDecodeError:
            response_data = {
                'status': 'error',
                'message': 'Ошибка при разборе данных JSON.'
            }
            return JsonResponse(response_data, status=400)

    else:
        return JsonResponse({'error': 'Неверный метод запроса'})


def course_registration(request, course_id):
    course = Course.objects.get(id=course_id)
    user = request.user
    course_teacher = course.teacher
    if user != course_teacher:
        CourseUser.objects.create(user=user, course=course)
        assignments = Assignment.objects.filter(course=course)
        for assignment in assignments:
            AssignmentSubmission.objects.create(assignment=assignment, student=user)

    context = {'course': course}
    return render(request, 'courses/course_registration.html', context)


def assignment_view(request, course_id, assignment_id):
    course = Course.objects.get(id=course_id)
    assignment = Assignment.objects.get(id=assignment_id, course=course)
    student = request.user
    try:
        assignment_submission = AssignmentSubmission.objects.get(student=student, assignment=assignment)
    except AssignmentSubmission.DoesNotExist:
        assignment_submission = AssignmentSubmission.objects.create(assignment=assignment, student=student)

    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES, instance=assignment_submission)
        if form.is_valid():
            form.save(commit=False)
            form.instance.assignment = assignment
            form.instance.student = student
            form.instance.status = 's'
            form.save()
            messages.success(request, _('Файл успешно добавлен, Ваш преподаватель скоро его проверит.'))
        else:
            messages.error(request,
                           _('Произошла ошибка, возможно, Вы пытались прикрепить файл с запрещенным расширением.'))
        return redirect('courses:assignment_view', course_id=course_id, assignment_id=assignment_id)

    else:
        form = AssignmentSubmissionForm(initial={'assignment': assignment, 'student': student})
        context = {
            'course': course,
            'assignment': assignment,
            'assignment_submission': assignment_submission,
            'form': form
        }
        return render(request, 'courses/assignment_page.html', context)


def assignment_check(request, assignment_submission_id):
    assignment_submission = AssignmentSubmission.objects.get(id=assignment_submission_id)
    assignment = assignment_submission.assignment
    student = assignment_submission.student
    course = assignment.course
    if request.method == 'POST':
        form = AssignmentSubmissionTeacherCheckForm(request.POST, instance=assignment_submission)
        if form.is_valid():
            form.save(commit=False)
            if form.instance.earned_mark == 0:
                form.instance.status = 'r'
            else:
                form.instance.status = 'f'
                form.instance.is_finished = True
            form.save()
            messages.success(request, _('Комментарий к работе студента успешно создан.'))
        else:
            messages.error(request, _('Упс, что-то пошло не так!'))
        return redirect('courses:course_main_page', course_id=course.id)

    else:
        initial = {'assignment': assignment, 'student': student, 'earned_mark': 0}
        form = AssignmentSubmissionTeacherCheckForm(initial=initial)
        context = {
            'form': form,
            'assignment_submission': assignment_submission,
            'course': course
        }
        return render(request, 'courses/assignment_check.html', context)
