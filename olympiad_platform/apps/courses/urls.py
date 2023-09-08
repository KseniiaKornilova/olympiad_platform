from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('courses/list/', views.UserCoursesList.as_view(), name='courses_list'),
    path('courses/', views.CourseList.as_view(), name='courses'),
]