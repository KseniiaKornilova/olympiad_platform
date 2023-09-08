from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course
from ..olympiads.models import Subject
from ..olympiads.forms import SearchForm

# Create your views here.

class UserCoursesList(ListView):
    model = Course
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        queryset = self.request.user.course_set.all()
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


