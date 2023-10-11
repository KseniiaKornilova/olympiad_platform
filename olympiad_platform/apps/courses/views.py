import subprocess
import os
import re
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course, Lesson, CourseUser, Assignment, AssignmentSubmission
from ..olympiads.models import Subject
from ..olympiads.forms import SearchForm

# Create your views here.

class UserCoursesList(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = self.request.user.course_participants.all()
        search_word = self.request.GET.get('keyword')
        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchForm(self.request.GET)
        return context


class CourseList(ListView):
    template_name = 'courses/all_courses.html'
    model = Course
    context_object_name = 'courses'

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        school_subject = self.request.GET.get('subject', None)
        search_word = self.request.GET.get('keyword')
        queryset = Course.objects.all()
        if category:
            queryset = queryset.filter(category__exact=category)
        if school_subject:
            queryset = queryset.filter(subject__exact=school_subject)
        if search_word:
            queryset = queryset.filter(title__icontains=search_word)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.all()
        context['form'] = SearchForm(self.request.GET)
        return context


def course_main_page(request, course_id):
    student = request.user
    course = Course.objects.get(id=course_id)
    course_submission = CourseUser.objects.get(user=student, course=course)
    try:
        assignments = Assignment.objects.filter(course=course)
    except Assignment.DoesNotExist:
        assignments = None

    try:
        assignment_submissions = AssignmentSubmission.objects.filter(assignment__course=course, student=student)
    except AssignmentSubmission.DoesNotExist:
        assignment_submissions = None

    try:
        lessons = Lesson.objects.filter(course=course).order_by('number')
    except Lesson.DoesNotExist:
        lessons = None

    context = {'student': student, 
                'course': course, 
                'course_submission': course_submission, 
                'assignments': assignments, 
                'assignment_submissions': assignment_submissions,
                'lessons': lessons}

    return render (request, 'courses/course_main_page.html', context)


def lesson_view(request, course_id, lesson_id):
    asciidoc_filename = f'course{course_id}_lesson{lesson_id}.adoc'
    asciidoc_directory = os.path.join(os.path.dirname(__file__), 'adoc_files')
    asciidoc_file_path = os.path.join(asciidoc_directory, asciidoc_filename)

    if not os.path.exists(asciidoc_file_path):
        return HttpResponse("Материал урока еще не создан", status=404)

    command = ['asciidoctor', '-o', '-', asciidoc_file_path]
    html_content = subprocess.check_output(command, universal_newlines=True)

    footer_pattern = r'<div id="footer">.*?</div>'
    html_content_without_footer = re.sub(footer_pattern, '', html_content, flags=re.DOTALL)

    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id)
    lessons = Lesson.objects.filter(course=course).order_by('number')
    context = {'course': course, 
                'lesson': lesson, 
                'lessons': lessons,
                'html_content': html_content_without_footer}
    return render(request, 'courses/lesson_page.html', context)



