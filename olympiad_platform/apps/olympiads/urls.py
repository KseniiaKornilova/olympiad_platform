from django.urls import path, include
from . import views

app_name = 'olympiads'

urlpatterns = [
    path('', views.index, name='index'),
    path('olympiads/', views.OlympiadList.as_view(), name='olympiads'),
    path('olympiads/list/', views.UserOlympiadList.as_view(), name='olympiads_list'),
    path('olympiads/list/previous', views.UserPreviousOlympiadList.as_view(), name='previous_list'),
    path('olympiads/list/coming', views.UserComingOlympiadList.as_view(), name='coming_list'),
    path('olympiads/<int:olympiad_id>/<int:user_id>/', views.olympiad_page, name='olympiad_page'),
    path('olympiads/registration/<int:olympiad_id>/', views.olympiad_registration, name='olympiad_registration'),
]