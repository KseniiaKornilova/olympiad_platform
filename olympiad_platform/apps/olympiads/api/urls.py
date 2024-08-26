from django.urls import path
from . import views


app_name = 'olympiads'

urlpatterns = [
    path('olympiads/', views.OlympiadListView.as_view(), name='olympiad_list'),
    path('olympiads/<int:pk>/', views.OlympiadDetailView.as_view(), name='olympiad_detail'),
    path('olympiads/<int:pk>/enroll/', views.OlympiadEnrollView.as_view(), name='olympiad_enroll'),
    path('olympiads/<int:pk>/unenroll/', views.OlympiadUnenrollView.as_view(), name='olympiad_unenroll')
]
