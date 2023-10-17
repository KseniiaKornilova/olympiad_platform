from datetime import date, datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from ..students.models import User
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
    pass


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