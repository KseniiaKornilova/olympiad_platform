from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import ChangeInfoForm, ChangePasswordForm, LoginForm, ResetPasswordConfirmForm, ResetPasswordForm, UserForm
from .models import User


class UserLogin(LoginView):
    form_class = LoginForm
    template_name = 'students/login.html'


@login_required
def profile(request):
    return render(request, 'students/profile.html')


class UserLogout(LogoutView, LoginRequiredMixin):
    template_name = 'students/logout.html'


class UserRegister(CreateView):
    model = User
    template_name = 'students/register_user.html'
    form_class = UserForm
    success_url = reverse_lazy('students:register_done')

    def form_valid(self, form):
        super().form_valid(form)
        backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object, backend=backend)
        return redirect(self.success_url)


class UserRegisterDone(TemplateView):
    template_name = 'students/register_done.html'


class UserChangeInfo(SuccessMessageMixin, UpdateView, LoginRequiredMixin):
    model = User
    form_class = ChangeInfoForm
    template_name = 'students/change_info.html'
    success_url = reverse_lazy('students:profile')
    success_message = 'Редактирование профиля успешно завершено'

# получение записи пользователя из БД
    def get_object(self, queryset=None):
        return self.request.user


class UserChangePassword(SuccessMessageMixin, PasswordChangeView, LoginRequiredMixin):
    template_name = 'students/password_change.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('students:profile')
    success_message = 'Пароль успешно изменен'


class UserDeleteProfile(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('olympiads:index')
    template_name = 'students/delete_user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)


class PasswordReset(PasswordResetView):
    template_name = 'students/reset_password.html'
    form_class = ResetPasswordForm
    email_template_name = 'students/password_reset_email.html'
    success_url = reverse_lazy('students:password_reset_done')


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'students/password_reset_confirm.html'
    form_class = ResetPasswordConfirmForm
    success_url = reverse_lazy('students:password_reset_complete')
    post_reset_login = True


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'students/reset_password_done.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'students/reset_password_complete.html'
