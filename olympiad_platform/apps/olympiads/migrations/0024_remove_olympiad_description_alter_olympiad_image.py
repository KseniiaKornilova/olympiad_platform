# Generated by Django 4.2.13 on 2024-08-15 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olympiads', '0023_olympiad_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='olympiad',
            name='description',
        ),
        migrations.AlterField(
            model_name='olympiad',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/olympiads/', verbose_name='Изображение'),
        ),
    ]