from django.urls import path
from . import views

app_name = 'olympiads'

urlpatterns = [
    path('', views.index, name='index'),
    path('is_not_ready/', views.is_not_ready, name='is_not_ready'),
    path('olympiads/', views.OlympiadList.as_view(), name='olympiads'),
    path('olympiads/list/', views.UserOlympiadList.as_view(), name='olympiads_list'),
    path('olympiads/list/previous', views.UserPreviousOlympiadList.as_view(), name='previous_list'),
    path('olympiads/list/coming', views.UserComingOlympiadList.as_view(), name='coming_list'),
    path('olympiads/<int:olympiad_id>/', views.olympiad_page, name='olympiad_page'),
    path('olympiads/submit_o_question_answer', views.submit_o_question_answer, name='submit_o_question_answer'),
    path('olympiads/submit_t_question_answer', views.submit_t_question_answer, name='submit_t_question_answer'),
    path('olympiads/submit_olympiad_answer/', views.submit_olympiad_answer, name='submit_olympiad_answer'),
    path('olympiads/get_template/', views.get_template_view, name='get_template'),
    path('olympiads/registration/<int:olympiad_id>/', views.olympiad_registration, name='olympiad_registration'),
]
