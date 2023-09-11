from django.urls import path, include
from . import views

app_name = 'olympiads'

urlpatterns = [
    path('', views.index, name='index'),
    path('olympiads/', views.OlympiadList.as_view(), name='olympiads'),
    path('olympiads/list/', views.UserOlympiadList.as_view(), name='olympiads_list'),
    path('olympiads/list/previous', views.UserPreviousOlympiadList.as_view(), name='previous_list'),
    path('olympiads/list/coming', views.UserComingOlympiadList.as_view(), name='coming_list'),
]