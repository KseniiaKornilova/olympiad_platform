from django.db import models
from ..students.models import User
from django.utils import timezone


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
    stage = models.CharField(max_length=100, verbose_name='Этап олимпиады', null=True, blank=True)
    degree = models.SmallIntegerField(verbose_name='Рекомендуемый класс обучения')
    date_of_start = models.DateTimeField(verbose_name='Начало проведения олимпиады')
    registration_dedline = models.DateTimeField(verbose_name='Дата окончания регистрации')
    olympiad_duration = models.DurationField(verbose_name='Продолжительность олимпиады')
    participants = models.ManyToManyField(User, through='OlympiadUser', verbose_name='Участники олимпиады')
    image = models.CharField(verbose_name='Путь до изображения от static директории', max_length=200, null=True, 
                             blank=True)
    
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
    total_mark = models.SmallIntegerField(null=True, blank=True, verbose_name='Максимально возможное количество баллов')
    ranking_place = models.SmallIntegerField(null=True, blank=True, verbose_name='Место участника в рейтинге')

    @classmethod
    def create(cls, user, olympiad):
        submission = cls(user=user, olympiad=olympiad)
        submission.save()
        return submission

    class Meta:
        verbose_name = 'Данные о прохождении участником олимпиады'
        verbose_name_plural = 'Данные о прохождениях участниками олимпиад'
        ordering = ['olympiad', 'user']


class QuestionSection(models.Model):
    section = models.SmallIntegerField(verbose_name='Номер раздела олимпиады')
    points = models.SmallIntegerField(verbose_name='Количество баллов')

    def __str__(self):
        return f'{self.section}'

    class Meta:
        verbose_name = 'Раздел олимпиады'
        verbose_name_plural = 'Разделы олимпиады'
        ordering = ['section',]


class Question(models.Model):
    question_description = models.TextField(verbose_name='Формулировка вопроса')
    section = models.ForeignKey(QuestionSection, on_delete=models.PROTECT, verbose_name='Раздел олимпиады')
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE, verbose_name='Олимпиада')
    possible_answers = models.TextField(verbose_name='Варианты ответов, перечисленные через ","', blank=True, null=True)
    correct_answer = models.CharField(max_length=100, verbose_name='Правильный ответ')

    def __str__(self):
        return f'{self.question_description}'

    class Meta:
        verbose_name = 'Вопрос олимпиады'
        verbose_name_plural = 'Вопросы олимпиады'
        ordering = ['olympiad', 'section']


class UserAnswer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Участник олимпиады')
    question = models.OneToOneField(Question, on_delete=models.PROTECT, verbose_name='Вопрос олимпиады')
    answer = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ответ участника')
    score = models.SmallIntegerField(verbose_name='Количество баллов за ответ')

    class Meta:
        verbose_name = 'Решение олимпиады'
        verbose_name_plural = 'Решения олимпиад'
        ordering = ['user']
