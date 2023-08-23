from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import UserForm

# Create your views here.

class UserLogin(LoginView):
    template_name = 'students/login.html'
    
@login_required  
def profile(request):
    return render(request, 'students/profile.html')


class UserLogout(LogoutView, LoginRequiredMixin):
    template_name = 'students/logout.html'