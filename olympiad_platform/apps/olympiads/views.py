from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from ..students.models import User
from .models import Olympiad

# Create your views here.

def index(request):
    return render(request, 'olympiads/index.html')


class UserOlympiadList(ListView):
    model = Olympiad
    template_name = 'olympiads/olympiads_list.html'
    ordering = '-date_of_start'
    context_object_name = 'olympiads'

    def get_queryset(self):
        return self.request.user.olympiad_set.all()