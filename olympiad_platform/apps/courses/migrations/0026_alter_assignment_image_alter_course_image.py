# Generated by Django 4.1.3 on 2023-10-27 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0025_alter_assignmentsubmission_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='image',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Путь до изображения от static директории'),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Путь до изображения от static директории'),
        ),
    ]
