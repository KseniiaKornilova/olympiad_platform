from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course
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


