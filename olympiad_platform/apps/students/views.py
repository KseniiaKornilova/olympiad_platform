from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import UserForm

# Create your views here.

class UserLogin(LoginView):
    template_name = 'students/login.html'
    
    
    