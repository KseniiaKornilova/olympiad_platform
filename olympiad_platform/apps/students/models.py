from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    LETTER = (
        ('a', 'A'),
        ('b', 'Б'),
        ('v', 'В'),
    )
    STATUS = (
        ('t', 'Учитель'),
        ('s', 'Ученик'),
    )
    email = models.EmailField(max_length=50, unique=True, blank=False, verbose_name='Электронная почта')
    username = models.CharField(max_length=50, unique=False, null=True, blank=True)
    last_name = models.CharField(max_length=150, blank=False, verbose_name='Фамилия')
    first_name = models.CharField(max_length=150, blank=False, verbose_name='Имя')
    patronymic = models.CharField(max_length=150, null=True, blank=True, verbose_name='Отчество')
    birthday = models.DateField(null=True, verbose_name='Дата рождения')
    status = models.CharField(max_length=1, choices=STATUS, null=True, verbose_name='Должность')
    degree = models.SmallIntegerField(null=True, blank=False, verbose_name='Класс')
    degree_id = models.CharField(max_length=1, choices=LETTER, null=True, verbose_name='Буква класса')
    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['status', 'degree', 'degree_id','last_name', 'first_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


