from django.urls import path, include
from .views import UserLogin, profile, UserLogout, UserRegister, UserRegisterDone

app_name = 'students'

urlpatterns = [
    path('accounts/login/', UserLogin.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'), 
    path('accounts/logout/', UserLogout.as_view(), name='logout'),
    path('accounts/register/', UserRegister.as_view(), name='register'),
    path('accounts/register/done', UserRegisterDone.as_view(), name='register_done'),
]