from apps.olympiads.models import Olympiad, OlympiadUser, Subject

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

import factory

User = get_user_model()


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject

    name = factory.Faker('word')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    status = 's'
    degree = factory.Faker('random_int', min=1, max=11)
    image = SimpleUploadedFile(name='test_user.jpg', content=b'', content_type='image/jpeg')


class OlympiadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Olympiad

    title = factory.Faker('sentence', nb_words=3)
    subject = factory.SubFactory(SubjectFactory)
    description = factory.Faker('text')
    stage = factory.Faker('random_element', elements=('Школьный', 'Областной', 'Всероссийский'))
    degree = factory.Faker('random_int', min=1, max=11)
    date_of_start = factory.LazyFunction(timezone.now)
    registration_dedline = factory.LazyFunction(lambda: timezone.now() + timezone.timedelta(days=5))
    total_mark = 100
    image = SimpleUploadedFile(name='test_olympiad.jpg', content=b'', content_type='image/jpeg')


class OlympiadUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OlympiadUser

    user = factory.SelfAttribute('..user')
    olympiad = factory.SelfAttribute('..olympiad')
    registration_date = factory.LazyFunction(timezone.now)
