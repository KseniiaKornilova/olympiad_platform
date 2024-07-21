from .models import Assignment, AssignmentSubmission, CourseUser
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


@receiver(post_save, sender=Assignment)
def update_course_mark(sender, instance, **kwargs):
    course = instance.course
    course.total_mark += instance.total_mark
    course.save()


@receiver(post_save, sender=AssignmentSubmission)
def update_user_course_mark(sender, instance, **kwargs):
    if instance.earned_mark > 0:
        course = instance.assignment.course
        user = instance.student
        course_submission = CourseUser.objects.get(user=user, course=course)
        course_submission.earned_mark += instance.earned_mark
        course_submission.save()


@receiver(pre_delete, sender=CourseUser)
def delete_assignments_submissions(sender, instance, **kwargs):
    student = instance.user
    course = instance.course
    AssignmentSubmission.objects.filter(student=student, assignment__course=course).delete()
