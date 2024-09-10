from apps.students.forms import ChangeInfoForm, ChangePasswordForm, LoginForm, ResetPasswordConfirmForm, UserForm

from django.contrib.auth import get_user_model

import pytest


User = get_user_model()


@pytest.fixture
def form_data():
    form_data = {
        'email': 'ivanov@gmail.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'patronymic': 'Иванович',
        'birthday': '2010-12-11',
        'status': 's',
        'degree': 10,
        'degree_id': 'a'
    }
    return form_data


@pytest.mark.django_db
def test_user_form_valid_data(form_data):
    form = UserForm(data=form_data)
    assert form.is_valid()

    user = form.save()
    assert user.email == form_data['email']
    assert user.check_password(form_data['password1'])


@pytest.mark.django_db
def test_user_form_necessary_field_not_filled(form_data):
    form_data.pop('first_name')
    form = UserForm(data=form_data)

    assert not form.is_valid()
    assert 'Обязательное поле.' in form.errors['first_name']


@pytest.mark.django_db
def test_user_form_invalid_passwords(form_data):
    form_data['password2'] = 'wrongpassword'

    form = UserForm(data=form_data)
    assert not form.is_valid()
    assert 'Пароли не совпадают' in form.errors['__all__']


@pytest.mark.django_db
def test_user_form_invalid_email(form_data):
    form_data['email'] = 'wrong-email@com'

    form = UserForm(data=form_data)
    assert not form.is_valid()
    assert 'Введите правильный адрес электронной почты.' in form.errors['email']


@pytest.mark.django_db
def test_user_form_password_too_short(form_data):
    form_data.update({'password1': 'short', 'password2': 'short'})

    form = UserForm(data=form_data)
    assert not form.is_valid()
    assert 'Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.' in form.errors['password1']


@pytest.mark.django_db
def test_user_form_password_digits_only(form_data):
    form_data.update({'password1': '123456789', 'password2': '123456789'})

    form = UserForm(data=form_data)
    assert not form.is_valid()
    assert 'Введённый пароль состоит только из цифр.' in form.errors['password1']


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='ivanov@gmail.com',
        password='testpassword123',
        first_name='Иван',
        last_name='Иванов',
        patronymic='Иванович',
        birthday='2010-12-11',
        status='s',
        degree=10,
        degree_id='a'
    )
    return user


@pytest.mark.django_db
def test_login_form_valid_data(test_user):
    form = LoginForm(data={
        'username': 'ivanov@gmail.com',
        'password': 'testpassword123'
    })

    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_password(test_user):
    form = LoginForm(data={
        'username': 'ivanov@gmail.com',
        'password': 'wrongpassword123'
    })

    assert not form.is_valid()
    assert any(['введите правильные Электронная почта и пароль.' in error for error in form.errors['__all__']])


@pytest.mark.django_db
def test_login_form_invalid_email(test_user):
    form = LoginForm(data={
        'username': 'wrongivanov@gmail.com',
        'password': 'testpassword123'
    })

    assert not form.is_valid()
    assert any(['введите правильные Электронная почта и пароль.' in error for error in form.errors['__all__']])


@pytest.mark.django_db
def test_change_info_valid_data(test_user, form_data):
    form_data.update({
        'first_name': 'Петр',
        'last_name': 'Петров',
        'patronymic': 'Петрович',
    })

    form = ChangeInfoForm(data=form_data, instance=test_user)
    assert form.is_valid()
    user = form.save()

    assert user.first_name == 'Петр'
    assert user.last_name == 'Петров'
    assert user.patronymic == 'Петрович'


@pytest.mark.django_db
def test_change_info_invalid_data(test_user, form_data):
    form_data['email'] = 'wrong-email@com'

    form = ChangeInfoForm(data=form_data, instance=test_user)
    assert not form.is_valid()
    assert 'email' in form.errors


@pytest.mark.django_db
def test_change_info_not_unique_email(test_user, form_data):
    User.objects.create_user(
        email='petrov@gmail.com',
        password='testpassword123',
        first_name='Петр',
        last_name='Петров',
        patronymic='Петрович',
        birthday='2010-12-11',
        status='s',
        degree=10,
        degree_id='a'
    )
    form_data['email'] = 'petrov@gmail.com'
    form = ChangeInfoForm(data=form_data, instance=test_user)
    assert not form.is_valid()
    assert 'Пользователь с таким email уже существует.' in form.errors['email']


@pytest.mark.django_db
def test_change_password_form_valid(test_user):
    form = ChangePasswordForm(user=test_user, data={
        'old_password': 'testpassword123',
        'new_password1': 'newstrongpassword123',
        'new_password2': 'newstrongpassword123'
    })
    assert form.is_valid()
    updated_user = form.save()
    updated_user.refresh_from_db()
    assert updated_user.check_password('newstrongpassword123')


@pytest.mark.django_db
def test_change_password_form_invalid_old_password(test_user):
    form = ChangePasswordForm(user=test_user, data={
        'old_password': 'wrongpassword',
        'new_password1': 'newstrongpassword123',
        'new_password2': 'newstrongpassword123'
    })
    assert not form.is_valid()
    assert 'Ваш старый пароль введен неправильно. Пожалуйста, введите его снова.' in form.errors['old_password']


@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_password1, new_password2, expected_error",
    [
        ("123456789", "123456789", "Введённый пароль состоит только из цифр."),
        ("short", "short", "Введённый пароль слишком короткий."),
        ("password1", "password2", "Введенные пароли не совпадают.")
    ]
)
def test_change_password_form_invalid_new_password(test_user, new_password1, new_password2, expected_error):
    form_data = {
        'old_password': 'testpassword123',
        'new_password1': new_password1,
        'new_password2': new_password2,
    }
    form = ChangePasswordForm(user=test_user, data=form_data)
    assert not form.is_valid()
    assert any([expected_error in error for error in form.errors['new_password2']])


@pytest.mark.django_db
def test_reset_password_confirm_form_valid(test_user):
    form_data = {
        'new_password1': 'newpassword123',
        'new_password2': 'newpassword123',
    }
    form = ResetPasswordConfirmForm(user=test_user, data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_password1, new_password2, expected_error",
    [
        ("123456789", "123456789", "Введённый пароль состоит только из цифр."),
        ("short", "short", "Введённый пароль слишком короткий."),
        ("password1", "password2", "Введенные пароли не совпадают.")
    ]
)
def test_reset_password_confirm_form_invalid_passwords(test_user, new_password1, new_password2, expected_error):
    form_data = {
        'new_password1': new_password1,
        'new_password2': new_password2,
    }
    form = ResetPasswordConfirmForm(user=test_user, data=form_data)
    assert not form.is_valid()
    assert any([expected_error in error for error in form.errors['new_password2']])
