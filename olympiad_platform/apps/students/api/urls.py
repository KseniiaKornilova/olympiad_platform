from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('students/signup/', views.UserRegistrationView.as_view(), name='signup'),
    path('students/profile/', views.UserProfileUpdateView.as_view(), name='profile-update'),
]
