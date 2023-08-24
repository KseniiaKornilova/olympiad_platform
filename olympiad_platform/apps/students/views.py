from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .forms import UserForm
from .models import User

# Create your views here.

class UserLogin(LoginView):
    template_name = 'students/login.html'


@login_required  
def profile(request):
    return render(request, 'students/profile.html')


class UserLogout(LogoutView, LoginRequiredMixin):
    template_name = 'students/logout.html'


class UserRegister(CreateView):
    model = User
    template_name = 'students/register_user.html'
    form_class = UserForm
    success_url = reverse_lazy('students:register_done')


class UserRegisterDone(TemplateView):
    template_name = 'students/register_done.html'