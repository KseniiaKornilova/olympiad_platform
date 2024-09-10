from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('поле email является обязательным к заполнению')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь поле is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь поле is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    LETTER = (
        (None, 'Выберите букву Вашего класса'),
        ('a', 'A'),
        ('b', 'Б'),
        ('v', 'В'),
    )
    STATUS = (
        (None, 'Вы ученик или учитель?'),
        ('s', 'Ученик'),
        ('t', 'Учитель'),
    )
    email = models.EmailField(max_length=50, unique=True, verbose_name='Электронная почта')
    username = models.CharField(max_length=50, unique=False, null=True, blank=True)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    patronymic = models.CharField(max_length=150, null=True, blank=True, verbose_name='Отчество')
    birthday = models.DateField(null=True, verbose_name='Дата рождения')
    status = models.CharField(max_length=1, choices=STATUS, null=True, verbose_name='Должность')
    degree = models.SmallIntegerField(null=True, verbose_name='Класс')
    degree_id = models.CharField(max_length=1, choices=LETTER, null=True, verbose_name='Буква класса')
    image = models.ImageField(upload_to='images/users/', blank=True, null=True, verbose_name='Фото')

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['status', 'degree', 'degree_id', 'last_name', 'first_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
