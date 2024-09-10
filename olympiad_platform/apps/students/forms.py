from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

from .models import User


class UserForm(forms.ModelForm):
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={
       'class': 'form-control form-group',
       'placeholder': 'Email'
    }), help_text='Любые уведомления будут приходить на эту почту',
        error_messages={'unique': 'Пользователь с таким email уже существует.'})
    birthday = forms.DateField(label='День рождения', widget=forms.DateInput(
                                format=('%d-%m-%Y'),
                                attrs={
                                    'firstDay': 1, 'pattern': '\d{4}-\d{2}-\d{2}',
                                    'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date',
                                    'class': 'form-control form-group',
                                    'placeholder': 'День рождения'
                                }))
    degree = forms.IntegerField(label='Класс', min_value=1, max_value=11, widget=forms.NumberInput(attrs={
        'class': 'form-control form-group mb-3',
        'placeholder': 'Класс'
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-group',
        'placeholder': 'Пароль'
    }), help_text='Минимальная длина пароля - 8 символов, пароль должен включать как минимум 1 буквенный символ')
    password2 = forms.CharField(label='Введите пароль повторно', widget=forms.PasswordInput(attrs={
        'class': 'form-control form-group mb-3 mt-3',
        'placeholder': 'Пароль (повторно)'
    }))

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
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'email', 'birthday', 'status', 'degree', 'degree_id',
                  'password1', 'password2')

        widgets = {
            "last_name": forms.TextInput(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Фамилия'
            }),
            "first_name": forms.TextInput(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Имя'
            }),
            "patronymic": forms.TextInput(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Отчество'
            }),
            "status": forms.Select(attrs={
                'class': 'form-control form-group mb-3 mt-3',
                'placeholder': '--'
            }),
            "degree_id": forms.Select(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Буква класса'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        "autofocus": True,
        'class': 'form-control form-group mb-3',
        'placeholder': 'Email'
        }))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            'class': 'form-control form-group mb-3',
            'placeholder': 'Пароль'
            }))


class ChangeInfoForm(forms.ModelForm):
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={
       'class': 'form-control form-group',
       'placeholder': 'Email'
    }), error_messages={'unique': 'Пользователь с таким email уже существует.'})
    degree = forms.IntegerField(label='Класс', min_value=1, max_value=11, widget=forms.NumberInput(attrs={
        'class': 'form-control form-group mb-3',
        'placeholder': 'Класс'
    }))

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'patronymic', 'email', 'birthday', 'status', 'degree', 'degree_id')

        widgets = {
            "last_name": forms.TextInput(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Фамилия'
            }),
            "first_name": forms.TextInput(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Имя'
            }),
            "patronymic": forms.TextInput(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Отчество'
            }),
            "birthday": forms.DateInput(attrs={
                'class': 'form-control form-group mb-3, mt-3',
                'placeholder': 'День рождения'
            }),
            "status": forms.Select(attrs={
                'class': 'form-control form-group mb-3 mt-3',
                'placeholder': '--'
            }),
            "degree_id": forms.Select(attrs={
                'class': 'form-control form-group mb-3',
                'placeholder': 'Буква класса'
            })
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                'class': 'form-control form-group mb-3',
                'placeholder': 'Старый пароль'
                }))

    new_password1 = forms.CharField(
        label=("New password"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': 'form-control form-group',
            'placeholder': 'Новый пароль'
            }),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': 'form-control form-group mb-3 mt-3',
            'placeholder': 'Подтвердите новый пароль'
            }))


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {
            'class': 'form-control form-group mb-3 mt-3',
            'placeholder': 'Email'
        }


class ResetPasswordConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control form-group mb-3 mt-3',
            'placeholder': 'Новый пароль'
        })
        self.fields['new_password1'].help_text = 'Минимальная длина пароля - 8 символов, пароль должен включать \
                                                    как минимум 1 буквенный символ'
        self.fields['new_password2'].widget.attrs = {
            'class': 'form-control form-group mb-3 mt-3',
            'placeholder': 'Новый пароль (повторно)'
        }

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if new_password1:
            password_validation.validate_password(new_password1)
        return new_password1

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise ValidationError("Пароли не совпадают")
