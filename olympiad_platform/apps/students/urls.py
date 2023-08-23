from django.urls import path, include
from .views import UserLogin, profile, UserLogout

app_name = 'students'

urlpatterns = [
    path('accounts/login/', UserLogin.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'), 
    path('accounts/logout/', UserLogout.as_view(), name='logout'),
]