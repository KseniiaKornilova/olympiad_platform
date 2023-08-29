from django.urls import path, include
from .views import UserLogin, profile, UserLogout, UserRegister, UserRegisterDone, UserChangeInfo, UserChangePassword, UserDeleteProfile

app_name = 'students'

urlpatterns = [
    path('accounts/login/', UserLogin.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'), 
    path('accounts/logout/', UserLogout.as_view(), name='logout'),
    path('accounts/register/', UserRegister.as_view(), name='register'),
    path('accounts/register/done/', UserRegisterDone.as_view(), name='register_done'),
    path('accounts/profile_change/', UserChangeInfo.as_view(), name='profile_change'),
    path('accounts/password/change/', UserChangePassword.as_view(), name='password_change'),
    path('accounts/profile/delete/', UserDeleteProfile.as_view(), name='profile_delete'),
]