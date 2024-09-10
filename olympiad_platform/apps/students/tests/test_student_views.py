from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import pytest

User = get_user_model()


@pytest.mark.django_db
def test_user_register_view(client):
    url = reverse_lazy('students:register')

    form_data = {
        'email': 'ivanov@gmail.com',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'birthday': '2010-12-11',
        'status': 's',
        'degree': 10,
        'degree_id': 'a'
    }

    response = client.post(url, form_data)

    if response.status_code != 302:
        print(response.context['form'].errors)

    user = User.objects.get(email='ivanov@gmail.com')
    assert user is not None
    assert user.is_authenticated

    assert response.status_code == 302
    assert response.url == reverse_lazy('students:register_done')


@pytest.mark.django_db
def test_user_register_view_invalid_data(client):
    url = reverse_lazy('students:register')

    form_data = {
        'email': 'ivanov@gmail.com',
        'password1': 'testpassword123',
        'password2': 'differentpassword123',
        'first_name': 'Иван',
        'last_name': 'Иванов',
        'birthday': '2010-12-11',
        'status': 's',
        'degree': 10,
        'degree_id': 'a'
    }

    response = client.post(url, form_data)
    assert response.status_code == 200  # Форма снова отображается с ошибками
    assert 'Пароли не совпадают' in response.content.decode('utf-8')

    user_exists = User.objects.filter(email='ivanov@gmail.com').exists()
    assert not user_exists


@pytest.fixture
def test_user():
    user = User.objects.create_user(
        email='ivanov@gmail.com',
        password='testpassword123',
        first_name='Иван',
        last_name='Иванов',
        birthday='2010-12-11',
        status='s',
        degree=10,
        degree_id='a'
    )
    return user


@pytest.mark.django_db
def test_login_view(client, test_user):
    url = reverse_lazy('students:login')
    response = client.post(url, {'username': 'ivanov@gmail.com', 'password': 'testpassword123'})

    assert response.status_code == 302
    assert response.url == reverse_lazy('students:profile')


@pytest.mark.django_db
def test_profile_view(client, test_user):
    url = reverse_lazy('students:login')
    response = client.post(url, {'username': 'ivanov@gmail.com', 'password': 'testpassword123'})

    url = reverse_lazy('students:profile')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_view(client, test_user):
    client.login(email='ivanov@gmail.com', password='testpassword123')
    url = reverse_lazy('students:logout')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_change_info_view_get(client, test_user):
    client.login(username='ivanov@gmail.com', password='testpassword123')

    url = reverse_lazy('students:profile_change')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_change_info_view(client, test_user):
    User.objects.create_user(
        email='petrov@gmail.com',
        password='testpassword123',
        first_name='Петр',
        last_name='Петров',
        birthday='2010-12-11',
        status='s',
        degree=10,
        degree_id='a'
    )

    client.login(username='ivanov@gmail.com', password='testpassword123')

    url = reverse_lazy('students:profile_change')
    updated_data = {
        'email': 'ivanov@gmail.com',
        'password1': 'testpassword123',
        'password2': 'differentpassword123',
        'first_name': 'Петр',
        'last_name': 'Иванов',
        'birthday': '2010-12-11',
        'status': 's',
        'degree': 10,
        'degree_id': 'a'
    }
    response = client.post(url, updated_data)

    assert response.status_code == 302
    assert response.url == reverse_lazy('students:profile')

    test_user.refresh_from_db()
    assert test_user.first_name == 'Петр'

    updated_data.update({'email': 'petrov@gmail.com'})
    response = client.post(url, updated_data)

    assert response.status_code == 200
    assert 'Пользователь с таким email уже существует.' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_password_change_view_get(client, test_user):
    client.login(username='ivanov@gmail.com', password='testpassword123')

    url = reverse_lazy('students:password_change')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_password_change_view_valid_password(client, test_user):
    client.login(username='ivanov@gmail.com', password='testpassword123')

    url = reverse_lazy('students:password_change')
    form_data = {
        'old_password': 'testpassword123',
        'new_password1': 'newtestpassword123',
        'new_password2': 'newtestpassword123',
    }
    response = client.post(url, form_data)

    assert response.status_code == 302
    assert response.url == reverse_lazy('students:profile')

    test_user.refresh_from_db()
    assert test_user.check_password('newtestpassword123')


@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_password1, new_password2, expected_error",
    [
        ("123456789", "123456789", "Введённый пароль состоит только из цифр."),
        ("short", "short", "Введённый пароль слишком короткий. "),
        ("password1", "password2", "Введенные пароли не совпадают.")
    ]
)
def test_password_change_view_invalid_passwords(client, test_user, new_password1, new_password2, expected_error):
    client.login(username='ivanov@gmail.com', password='testpassword123')

    url = reverse_lazy('students:password_change')
    form_data = {
        'old_password': 'testpassword123',
        'new_password1': new_password1,
        'new_password2': new_password2,
    }
    response = client.post(url, form_data)

    assert response.status_code == 200
    assert expected_error in response.content.decode('utf-8')


@pytest.mark.django_db
def test_delete_profile_view(client, test_user):
    client.login(username='ivanov@gmail.com', password='testpassword123')

    url = reverse_lazy('students:profile_delete')
    response = client.post(url)

    assert response.status_code == 302
    assert response.url == reverse_lazy('olympiads:index')

    with pytest.raises(User.DoesNotExist):
        User.objects.get(email=test_user.email)


@pytest.mark.django_db
def test_password_reset_view_get(client):
    url = reverse_lazy('students:password_reset')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_password_reset_view_post(client, test_user):
    url = reverse_lazy('students:password_reset')
    response = client.post(url, {'email': 'ivanov@gmail.com'})

    assert response.status_code == 302
    assert response.url == reverse_lazy('students:password_reset_done')

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ['ivanov@gmail.com']


@pytest.mark.django_db
def test_password_reset_confirm_view_post(client, test_user):
    token = default_token_generator.make_token(test_user)
    uid = urlsafe_base64_encode(force_bytes(test_user.pk))

    url = reverse_lazy('students:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

    get_response = client.get(url)
    new_password = 'newpassword123'
    post_response = client.post(get_response.url, {'new_password1': new_password, 'new_password2': new_password})

    assert post_response.status_code == 302
    assert post_response.url == reverse_lazy('students:password_reset_complete')

    test_user.refresh_from_db()
    assert test_user.check_password(new_password)
