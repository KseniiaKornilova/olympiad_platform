# Generated by Django 4.2.13 on 2024-07-21 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olympiads', '0020_rename_marks_truefalsequestion_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='olympiad',
            name='total_mark',
            field=models.SmallIntegerField(default=0, verbose_name='Максимально возможное количество баллов'),
        ),
    ]