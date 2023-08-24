from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import User

class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', 
        help_text='Любые уведомления будут приходить на эту почту') 
    degree = forms.IntegerField(label='Класс', min_value=1, max_value=11)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, 
        help_text='Минимальная длина пароля - 8 символов, пароль должен включать как минимум 1 буквенный символ')
    password2 = forms.CharField(label='Введите пароль повторно', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
            return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают!')
        

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'email', 'birthday', 'status', 'degree', 'degree_id', 'password1', 'password2')
