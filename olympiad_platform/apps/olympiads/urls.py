from django.urls import path, include
from . import views

app_name = 'olympiads'

urlpatterns = [
    path('', views.index, name='index'),
]