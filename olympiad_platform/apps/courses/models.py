import os
from django.db import models
from django.core import validators
from ..olympiads.models import Subject
from ..students.models import User


class Course(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название курса')
    course_description = models.TextField(verbose_name='Описание курса', blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Название дисциплины')
    category = models.CharField(verbose_name='Категория учащихся', max_length=150, blank=True, null=True)
    month_amount = models.SmallIntegerField(verbose_name='Продолжительность курса', blank=True, null=True)
    times_a_week = models.SmallIntegerField(verbose_name='Количество уроков в неделю', blank=True, null=True)
    price = models.IntegerField(verbose_name='Стоимость курса', blank=True, null=True)
    total_mark = models.IntegerField(default=0, verbose_name='Максимально возможное количество баллов')
    participants = models.ManyToManyField(User, through='CourseUser', verbose_name='Ученики курса',
                                          related_name='course_participants')
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, related_name='course_teacher',
                                verbose_name='Учитель курса', null=True, blank=True)
    image = models.CharField(verbose_name='Путь до изображения от static директории',
                             max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['subject', 'title']


class CourseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя ученика')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    is_finished = models.BooleanField(null=True, blank=True, default=False,
                                      verbose_name='Участник выполнил все задания?')
    earned_mark = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name='Количество набранных баллов')

    class Meta:
        verbose_name = 'Прохождение курса учеником'
        verbose_name_plural = 'Прохождения курсов учениками'


class Lesson(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название урока')
    number = models.SmallIntegerField(verbose_name='Номер урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса')
    content = models.TextField(blank=True, null=True, verbose_name='Содержание урока')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Assignment(models.Model):
    assignment_num = models.SmallIntegerField(validators=[validators.MinValueValidator(1)],
                                              verbose_name='Номер задания')
    title = models.CharField(max_length=100, verbose_name='Название задания')
    description = models.TextField(verbose_name='Описание задания')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс, к которому относится задание')
    total_mark = models.SmallIntegerField(verbose_name='Максимально возможное количество баллов')
    image = models.CharField(verbose_name='Путь до изображения от static директории', max_length=200,
                             null=True, blank=True)

    def __str__(self):
        return f'{self.course} : {self.title}'

    class Meta:
        verbose_name = 'Задание курса'
        verbose_name_plural = 'Задания курсов'


def upload_homework(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    new_filename = (f'{instance.student.last_name}_{instance.student.first_name}_'
                    f'{instance.assignment.course.title}_{instance.assignment.title}{file_extension}')
    upload_path = os.path.join('homework_files', new_filename)
    return upload_path


STATUS = (
        ('-', 'Студент не начал работу'),
        ('s', 'Ждет проверку'),
        ('r', 'Получено ревью задания'),
        ('f', 'Выполнено'),
    )


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Задание курса')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    earned_mark = models.SmallIntegerField(validators=[validators.MinValueValidator(0)],
                                           verbose_name='Количество полученных баллов за задание', default=0)
    status = models.CharField(max_length=1, default='-', choices=STATUS, null=True, blank=True,
                              verbose_name='Статус выполнения задания')
    is_finished = models.BooleanField(default=False, verbose_name='Задание засчитано?')
    homework_file = models.FileField(verbose_name='Файл с решением', null=True, blank=True, upload_to=upload_homework)
    teacher_comment = models.TextField(verbose_name='Комментарий преподавателя', null=True, blank=True)

    def __str__(self):
        return f'{self.assignment} : {self.student}'

    class Meta:
        verbose_name = 'Решение задания курса'
        verbose_name_plural = 'Решения заданий курсов'


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', blank=True)
    student = models.CharField(max_length=100, verbose_name='Автор комментария')
    content = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateField(verbose_name='Дата публикации комментария')

    def __str__(self):
        return f'{self.author} : {self.content}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
