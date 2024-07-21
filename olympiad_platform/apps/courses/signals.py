from .models import Assignment
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Assignment)
def update_course_mark(sender, instance, **kwargs):
    course = instance.course
    course.total_mark += instance.total_mark
    course.save()
