from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from ..students.models import User
from .models import Olympiad, Subject
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