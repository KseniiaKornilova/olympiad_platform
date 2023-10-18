from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('courses/list/', views.UserCoursesList.as_view(), name='courses_list'),
    path('courses/', views.CourseList.as_view(), name='courses'),
    path('courses/<int:course_id>/', views.course_main_page, name='course_main_page'),
    path('courses/<int:course_id>/<int:lesson_id>/', views.lesson_view, name='lesson_view'),
    path('courses/<int:course_id>/<int:lesson_id>/comments/', views.lesson_comment_view, name='lesson_comment_page'),
    path('courses/comments/', views.submit_comment, name='submit_comment'),
    path('courses/registration/<int:course_id>', views.course_registration, name='courses_registration'),
]