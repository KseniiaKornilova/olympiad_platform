from django.db import models
from django.conf import settings
from django.core import validators
from ..olympiads.models import Subject, Olympiad
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
    participants = models.ManyToManyField(User, through='CourseUser', verbose_name='Ученики курса', related_name='course_participants')
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, related_name='course_teacher', verbose_name='Учитель курса', null=True, blank=True)
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
    is_finished = models.BooleanField(null=True, blank=True, default=False, verbose_name='Участник выполнил все задания?')
    earned_mark = models.SmallIntegerField(null=True, blank=True, verbose_name='Количество набранных баллов')
    total_mark = models.SmallIntegerField(null=True, blank=True, verbose_name='Максимально возможное количество баллов')
    percent_mark = models.FloatField(validators=[validators.MinValueValidator(0)], default=0, null=True, blank=True, verbose_name='% выполнения курса')
    class Meta: 
        verbose_name = 'Прохождение курса учеником'
        verbose_name_plural = 'Прохождения курсов учениками'


class Lesson(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Название урока')
    number = models.SmallIntegerField(verbose_name='Номер урока') 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Название курса')
    def __str__(self):
        return f'{self.title}'

    class Meta: 
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Assignment(models.Model):
    assignment_num = models.SmallIntegerField(validators=[validators.MinValueValidator(1)], verbose_name='Номер задания')
    title = models.CharField(max_length=100, verbose_name='Название задания')
    description = models.CharField(max_length=200, verbose_name='Описание задания')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс, к которому относится задание')
    total_mark = models.SmallIntegerField(verbose_name='Максимально возможное количество баллов')
    image = models.CharField(verbose_name='Путь до изображения от static директории', null=True, blank=True)

    def __str__(self):
        return f'{self.course} : {self.assignment_num}'

    class Meta:
        verbose_name = 'Задание курса'
        verbose_name_plural = 'Задания курсов'


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name='Задание курса')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    earned_mark = models.SmallIntegerField(validators=[validators.MinValueValidator(0)], verbose_name='Количество полученных баллов за задание')
    is_finished = models.BooleanField(default=False, verbose_name='Задание отправлено на проверку?')

    def __str__(self):
        return f'{self.assignment} : {self.student}'

    class Meta:
        verbose_name = 'Решение задания курса'
        verbose_name_plural = 'Решения заданий курсов'



class MultipleChoiceQuestion(models.Model):
    question_num = models.SmallIntegerField(verbose_name='Номер вопроса', validators=[validators.MinValueValidator(1)])
    title = models.CharField(verbose_name='Название вопроса', max_length=50)
    description = models.CharField(verbose_name='Формулировка вопроса', max_length=200)
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
    mark = models.SmallIntegerField(verbose_name='Баллы за вопрос', validators=[validators.MinValueValidator(1)])
    question_type = settings.MULTIPLECHOICE_QUESTION_TYPE
    olympiad = models.ForeignKey(Olympiad, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Вопрос для какой олимпиады')
    assignment = models.ForeignKey(Assignment, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Вопрос для какого задания')

    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = 'Вопрос с множественным ответом'
        verbose_name_plural = 'Вопросы с множественным ответом'


class MultipleChoiceSubmission(models.Model):
    a = models.BooleanField(default=False)
    b = models.BooleanField(default=False)
    c = models.BooleanField(default=False)
    d = models.BooleanField(default=False)
    e = models.BooleanField(default=False)
    f = models.BooleanField(default=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')
    students_mark = models.SmallIntegerField(default=0, validators=[validators.MinValueValidator(0)], verbose_name='Баллы студента за ответ')

    @classmethod
    def create(cls, a, b, c, d, e, f, student, question, students_mark):
        submission = cls(a=a, b=b, c=c, d=d, e=e, f=f, student=student, question=question, students_mark=students_mark)
        submission.save()
        return submission

    def __str__(self):
        return f'{self.student} : {self.question}'

    class Meta:
        verbose_name = 'Ответ на вопрос с множественным ответом'
        verbose_name_plural = 'Ответы на вопрос с множественным ответом'


class OneChoiceQuestion(models.Model):
    question_num = models.SmallIntegerField(verbose_name='Номер вопроса', validators=[validators.MinValueValidator(1)])
    title = models.CharField(verbose_name='Название вопроса', max_length=50)
    description = models.CharField(verbose_name='Формулировка вопроса', max_length=200)
    a = models.CharField(max_length=255, null=True)
    a_is_correct = models.BooleanField(default=False)
    b = models.CharField(max_length=255, null=True)
    b_is_correct = models.BooleanField(default=False)
    c = models.CharField(max_length=255, null=True, blank=True)
    c_is_correct = models.BooleanField(default=False)
    d = models.CharField(max_length=255, null=True, blank=True)
    d_is_correct = models.BooleanField(default=False)
    mark = models.SmallIntegerField(verbose_name='Баллы за вопрос', validators=[validators.MinValueValidator(1)])
    question_type = settings.ONECHOICE_QUESTION_TYPE
    olympiad = models.ForeignKey(Olympiad, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Вопрос для какой олимпиады')
    assignment = models.ForeignKey(Assignment, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Вопрос для какого задания')
    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = 'Вопрос с одним ответом'
        verbose_name_plural = 'Вопросы с одним ответом'


class OneChoiceSubmission(models.Model):
    a = models.BooleanField(default=False)
    b = models.BooleanField(default=False)
    c = models.BooleanField(default=False)
    d = models.BooleanField(default=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    question = models.ForeignKey(OneChoiceQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')
    students_mark = models.SmallIntegerField(default=0, validators=[validators.MinValueValidator(0)], verbose_name='Баллы студента за ответ')

    @classmethod
    def create(cls, a, b, c, d, student, question, students_mark):
        submission = cls(a=a, b=b, c=c, d=d, student=student, question=question, students_mark=students_mark)
        submission.save()
        return submission

    def __str__(self):
        return f'{self.student} : {self.question}'

    class Meta:
        verbose_name = 'Ответ на вопрос с одним ответом'
        verbose_name_plural = 'Ответы на вопрос с одним ответом'

# какое из утверждений верно
class TrueFalseQuestion(models.Model):
    question_num = models.SmallIntegerField(validators=[validators.MinValueValidator(1)], verbose_name='Номер вопроса')
    title = models.CharField(max_length=50, verbose_name='Название вопроса')
    description = models.CharField(max_length=150, verbose_name='Формулировка вопроса')
    true_choice = models.CharField(max_length=150, null=True, verbose_name='Правильное утверждение')
    false_choice = models.CharField(max_length=150, null=True, verbose_name='Ложное утверждение')
    answer = models.BooleanField(default=False, 
    verbose_name='Ответ: True - если верно утверждение в true_choice, false - если в false_choice')
    marks = models.SmallIntegerField(validators=[validators.MinValueValidator(1)], verbose_name='Количество баллов за правильный ответ')
    question_type = settings.TRUEFALSE_QUESTION_TYPE
    assignment = models.ForeignKey(Assignment, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Вопрос для какого задания')
    olympiad = models.ForeignKey(Olympiad, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Вопрос для какой олимпиады')

    def __str__(self):
        return f'{self.description}'

    class Meta:
        verbose_name = 'Вопрос "Какое из утверждений верно"'
        verbose_name_plural = 'Вопросы "Какое из утверждений верно"'


class TrueFalseSubmission(models.Model):
    answer = models.BooleanField(default=False, verbose_name='Ответ студента в форме True/False')
    students_mark = models.SmallIntegerField(default=0, validators=[validators.MinValueValidator(0)], verbose_name='Баллы студента за ответ')
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Студент')
    question = models.ForeignKey(TrueFalseQuestion, on_delete=models.CASCADE, verbose_name='Вопрос')
    
    def __str__(self):
        return f'{self.student} : {self.question}'

    @classmethod
    def create(cls, student, question, answer, students_mark):
        submission = cls(student=student, question=question, answer=answer, students_mark=students_mark)
        submission.save()
        return submission

    class Meta:
        verbose_name = 'Ответ на вопрос "Какое из утверждений верно'
        verbose_name_plural = 'Ответы на вопросы "Какое из утверждений верно'


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок', blank=True)
    student = models.CharField(max_length=100, verbose_name='Автор комментария')
    content = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateField(verbose_name='Дата публикации комментария')
    def __str__(self):
        return f'{{ self.author }} : {{ self.content }}'

    class Meta: 
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

