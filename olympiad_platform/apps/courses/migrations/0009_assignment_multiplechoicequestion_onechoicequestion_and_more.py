# Generated by Django 4.2.3 on 2023-09-27 09:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('olympiads', '0010_remove_useranswer_question_remove_useranswer_user_and_more'),
        ('courses', '0008_course_teacher_alter_course_participants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_num', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер задания')),
                ('title', models.CharField(max_length=100, verbose_name='Название задания')),
                ('description', models.CharField(max_length=200, verbose_name='Описание задания')),
                ('total_mark', models.SmallIntegerField(verbose_name='Максимально возможное количество баллов')),
                ('image', models.CharField(blank=True, null=True, verbose_name='Путь до изображения от static директории')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Курс, к которому относится задание')),
            ],
            options={
                'verbose_name': 'Задание курса',
                'verbose_name_plural': 'Задания курсов',
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_num', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер вопроса')),
                ('title', models.CharField(max_length=50, verbose_name='Название вопроса')),
                ('description', models.CharField(max_length=200, verbose_name='Формулировка вопроса')),
                ('a', models.CharField(max_length=255, null=True)),
                ('a_is_correct', models.BooleanField(default=False)),
                ('b', models.CharField(max_length=255, null=True)),
                ('b_is_correct', models.BooleanField(default=False)),
                ('c', models.CharField(blank=True, max_length=255, null=True)),
                ('c_is_correct', models.BooleanField(default=False)),
                ('d', models.CharField(blank=True, max_length=255, null=True)),
                ('d_is_correct', models.BooleanField(default=False)),
                ('e', models.CharField(blank=True, max_length=255, null=True)),
                ('e_is_correct', models.BooleanField(default=False)),
                ('f', models.CharField(blank=True, max_length=255, null=True)),
                ('f_is_correct', models.BooleanField(default=False)),
                ('mark', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Баллы за вопрос')),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.assignment', verbose_name='Вопрос для какого задания')),
                ('olympiad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='olympiads.olympiad', verbose_name='Вопрос для какой олимпиады')),
            ],
            options={
                'verbose_name': 'Вопрос с множественным ответом',
                'verbose_name_plural': 'Вопросы с множественным ответом',
            },
        ),
        migrations.CreateModel(
            name='OneChoiceQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_num', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер вопроса')),
                ('title', models.CharField(max_length=50, verbose_name='Название вопроса')),
                ('description', models.CharField(max_length=200, verbose_name='Формулировка вопроса')),
                ('a', models.CharField(max_length=255, null=True)),
                ('a_is_correct', models.BooleanField(default=False)),
                ('b', models.CharField(max_length=255, null=True)),
                ('b_is_correct', models.BooleanField(default=False)),
                ('c', models.CharField(blank=True, max_length=255, null=True)),
                ('c_is_correct', models.BooleanField(default=False)),
                ('d', models.CharField(blank=True, max_length=255, null=True)),
                ('d_is_correct', models.BooleanField(default=False)),
                ('mark', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Баллы за вопрос')),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.assignment', verbose_name='Вопрос для какого задания')),
                ('olympiad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='olympiads.olympiad', verbose_name='Вопрос для какой олимпиады')),
            ],
            options={
                'verbose_name': 'Вопрос с одним ответом',
                'verbose_name_plural': 'Вопросы с одним ответом',
            },
        ),
        migrations.CreateModel(
            name='TrueFalseQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_num', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер вопроса')),
                ('title', models.CharField(max_length=50, verbose_name='Название вопроса')),
                ('description', models.CharField(max_length=150, verbose_name='Формулировка вопроса')),
                ('true_choice', models.CharField(max_length=150, null=True, verbose_name='Правильное утверждение')),
                ('false_choice', models.CharField(max_length=150, null=True, verbose_name='Ложное утверждение')),
                ('answer', models.BooleanField(default=False, verbose_name='Ответ: True - если верно утверждение в true_choice, false - если в false_choice')),
                ('marks', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество баллов за правильный ответ')),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.assignment', verbose_name='Вопрос для какого задания')),
                ('olympiad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='olympiads.olympiad', verbose_name='Вопрос для какой олимпиады')),
            ],
            options={
                'verbose_name': 'Вопрос "Какое из утверждений верно',
                'verbose_name_plural': 'Вопросы "Какое из утверждений верно',
            },
        ),
        migrations.AlterModelOptions(
            name='courseuser',
            options={'verbose_name': 'Прохождение курса учеником', 'verbose_name_plural': 'Прохождения курсов учениками'},
        ),
        migrations.AddField(
            model_name='courseuser',
            name='earned_mark',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Количество набранных баллов'),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='is_finished',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Участник выполнил все задания?'),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='percent_mark',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='% выполнения курса'),
        ),
        migrations.AddField(
            model_name='courseuser',
            name='total_mark',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='Максимально возможное количество баллов'),
        ),
        migrations.CreateModel(
            name='TrueFalseSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField(default=False, verbose_name='Ответ студента в форме True/False')),
                ('students_mark', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Баллы студента за ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.truefalsequestion', verbose_name='Вопрос')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Ответ на вопрос "Какое из утверждений верно',
                'verbose_name_plural': 'Ответы на вопросы "Какое из утверждений верно',
            },
        ),
        migrations.CreateModel(
            name='OneChoiceSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.BooleanField(default=False)),
                ('b', models.BooleanField(default=False)),
                ('c', models.BooleanField(default=False)),
                ('d', models.BooleanField(default=False)),
                ('students_mark', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Баллы студента за ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.onechoicequestion', verbose_name='Вопрос')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Ответ на вопрос с одним ответом',
                'verbose_name_plural': 'Ответы на вопрос с одним ответом',
            },
        ),
        migrations.CreateModel(
            name='MultipleChoiceSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a', models.BooleanField(default=False)),
                ('b', models.BooleanField(default=False)),
                ('c', models.BooleanField(default=False)),
                ('d', models.BooleanField(default=False)),
                ('e', models.BooleanField(default=False)),
                ('f', models.BooleanField(default=False)),
                ('students_mark', models.SmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Баллы студента за ответ')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.multiplechoicequestion', verbose_name='Вопрос')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Ответ на вопрос с множественным ответом',
                'verbose_name_plural': 'Ответы на вопрос с множественным ответом',
            },
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earned_mark', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество полученных баллов за задание')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Задание отправлено на проверку?')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.assignment', verbose_name='Задание курса')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Решение задания курса',
                'verbose_name_plural': 'Решения заданий курсов',
            },
        ),
    ]