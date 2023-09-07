from django.db import models
from ..olympiads.models import Subject
from ..students.models import User

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название курса')
    course_description = models.TextField(verbose_name='Описание курса', blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Название дисциплины')
    category = models.CharField(verbose_name='Категория учащихся', max_length=150, blank=True, null=True)
    month_amount = models.SmallIntegerField(verbose_name='Продолжительность', blank=True, null=True)
    times_a_week = models.SmallIntegerField(verbose_name='Раз в неделю', blank=True, null=True)
    price = models.IntegerField(verbose_name='Стоимость курса', blank=True, null=True)
    participants = models.ManyToManyField(User, through='CourseUser', verbose_name='Ученики курса')
    image = models.CharField(verbose_name='Путь до изображения от static директории', null=True, blank=True)
    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['subject', 'title']


class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя ученика')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    class Meta: 
        verbose_name = 'Регистрация ученика на курс'
        verbose_name_plural = 'Регистрации учеников на курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название урока')
    number = models.SmallIntegerField(verbose_name='Номер урока') 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса')
    def __str__(self):
        return f'{self.title}'

    class Meta: 
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
