# Generated by Django 4.2.3 on 2023-10-13 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_rename_author_comment_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='lesson',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='courses.lesson', verbose_name='Урок'),
        ),
    ]