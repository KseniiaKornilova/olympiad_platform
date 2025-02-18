from django.core import validators
from django.db import models
from django.utils import timezone

from ..students.models import User


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название дисциплины')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Школьный предмет'
        verbose_name_plural = 'Школьные предметы'


class Olympiad(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название олимпиады')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Название дисциплины')
    description = models.TextField(blank=True, null=True, verbose_name='Описание олимпиады')
    stage = models.CharField(max_length=100, verbose_name='Этап олимпиады', null=True, blank=True)
    degree = models.SmallIntegerField(verbose_name='Рекомендуемый класс обучения')
    date_of_start = models.DateTimeField(verbose_name='Начало проведения олимпиады')
    registration_dedline = models.DateTimeField(verbose_name='Дата окончания регистрации')
    total_mark = models.SmallIntegerField(default=0, verbose_name='Максимально возможное количество баллов')
    participants = models.ManyToManyField(User, through='OlympiadUser', verbose_name='Участники олимпиады')
    image = models.ImageField(upload_to='images/olympiads/', blank=True, null=True, verbose_name='Изображение')

    def __str__(self):
        return f'{self.title}'

    def is_registrations_open(self):
        now = timezone.now()
        return self.registration_dedline > now

    class Meta:
        verbose_name = 'Олимпиада'
        verbose_name_plural = 'Олимпиады'
        ordering = ['subject', 'degree', 'title']


class OlympiadUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Имя участника')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name='Название олимпиады')
    registration_date = models.DateTimeField(null=True, verbose_name='Дата регистрации')
    is_finished = models.BooleanField(null=True, blank=True, default=False,
                                      verbose_name='Участник отправил ответы олимпиады на проверку?')
    earned_mark = models.SmallIntegerField(null=True, blank=True, verbose_name='Количество набранных баллов')
    ranking_place = models.SmallIntegerField(null=True, blank=True, verbose_name='Место участника в рейтинге')

    class Meta:
        verbose_name = 'Данные о прохождении участником олимпиады'
        verbose_name_plural = 'Данные о прохождениях участниками олимпиад'
        ordering = ['olympiad', 'user']


class BaseQuestion(models.Model):
    question_num = models.SmallIntegerField(verbose_name="Номер вопроса", validators=[validators.MinValueValidator(1)])
    title = models.CharField(verbose_name="Название вопроса", max_length=50)
    description = models.CharField(verbose_name="Формулировка вопроса", max_length=200)
    mark = models.SmallIntegerField(verbose_name="Баллы за вопрос", validators=[validators.MinValueValidator(1)])
    olympiad = models.ForeignKey(Olympiad, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Олимпиада")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.description}"


class BaseSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Студент")
    students_mark = models.SmallIntegerField(default=0, validators=[validators.MinValueValidator(0)],
                                             verbose_name="Баллы студента за ответ")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.student} : {self.question}"


class MultipleChoiceQuestion(BaseQuestion):
    a = models.CharField(max_length=255, null=True)
    a_is_correct = models.BooleanField(default=False)
    b = models.CharField(max_length=255, null=True)
    b_is_correct = models.BooleanField(default=False)
    c = models.CharField(max_length=255, null=True, blank=True)
    c_is_correct = models.BooleanField(default=False)
    d = models.CharField(max_length=255, null=True, blank=True)
    d_is_correct = models.BooleanField(default=False)
    e = models.CharField(max_length=255, null=True, blank=True)
    e_is_correct = models.BooleanField(default=False)
    f = models.CharField(max_length=255, null=True, blank=True)
    f_is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Вопрос с множественным ответом'
        verbose_name_plural = 'Вопросы с множественным ответом'


class MultipleChoiceSubmission(BaseSubmission):
    a = models.BooleanField(default=False)
    b = models.BooleanField(default=False)
    c = models.BooleanField(default=False)
    d = models.BooleanField(default=False)
    e = models.BooleanField(default=False)
    f = models.BooleanField(default=False)
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Ответ на вопрос с множественным ответом'
        verbose_name_plural = 'Ответы на вопрос с множественным ответом'


class OneChoiceQuestion(BaseQuestion):
    a = models.CharField(max_length=255, null=True)
    a_is_correct = models.BooleanField(default=False)
    b = models.CharField(max_length=255, null=True)
    b_is_correct = models.BooleanField(default=False)
    c = models.CharField(max_length=255, null=True, blank=True)
    c_is_correct = models.BooleanField(default=False)
    d = models.CharField(max_length=255, null=True, blank=True)
    d_is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Вопрос с одним ответом'
        verbose_name_plural = 'Вопросы с одним ответом'


class OneChoiceSubmission(BaseSubmission):
    a = models.BooleanField(default=False)
    b = models.BooleanField(default=False)
    c = models.BooleanField(default=False)
    d = models.BooleanField(default=False)
    question = models.ForeignKey(OneChoiceQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Ответ на вопрос с одним ответом'
        verbose_name_plural = 'Ответы на вопрос с одним ответом'


OPTION = (
        ('1', '1'),
        ('2', '2')
         )


class TrueFalseQuestion(BaseQuestion):
    first_statement = models.CharField(max_length=150, null=True, verbose_name='Первое утверждение')
    second_statement = models.CharField(max_length=150, null=True, verbose_name='Второе утверждение')
    answer = models.CharField(max_length=3, choices=OPTION, verbose_name='номер верного утверждения')

    class Meta:
        verbose_name = 'Вопрос "Какое из утверждений верно"'
        verbose_name_plural = 'Вопросы "Какое из утверждений верно"'


class TrueFalseSubmission(BaseSubmission):
    answer = models.CharField(max_length=3, null=True, verbose_name='Ответ студента (1 или 2)')
    question = models.ForeignKey(TrueFalseQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Ответ на вопрос "Какое из утверждений верно'
        verbose_name_plural = 'Ответы на вопросы "Какое из утверждений верно'
