from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

import pytest

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        email='ivanov@.com',
        password='password123',
        first_name='Иван',
        last_name='Иванов',
        status='s',
        degree=10,
        degree_id='a'
    )
    assert user.email == 'ivanov@.com'
    assert user.first_name == 'Иван'
    assert user.last_name == 'Иванов'
    assert user.status == 's'
    assert user.degree == 10
    assert user.degree_id == 'a'


@pytest.mark.django_db
def test_unique_email():
    User.objects.create_user(email='ivanov@.com', password='password123')
    with pytest.raises(IntegrityError):
        User.objects.create_user(email='ivanov@.com', password='password456')


@pytest.mark.django_db
def test_user_str():
    user = User.objects.create_user(
        email='ivanov@.com',
        first_name='Иван',
        last_name='Иванов',
        patronymic='Иванович'
    )
    assert str(user) == 'Иванов Иван Иванович'


@pytest.mark.django_db
def test_user_required_fields():
    user = User(email='ivanov@.com', last_name='Иванов')
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_user_status_choices():
    user = User(email='ivanov@.com', status='c')
    with pytest.raises(ValidationError):
        user.full_clean()


@pytest.mark.django_db
def test_user_image_upload():
    image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    user = User.objects.create_user(email='ivanov@.com', first_name='Иван', last_name='Иванов', image=image)
    assert user.image.name.startswith('images/users/test_image')
