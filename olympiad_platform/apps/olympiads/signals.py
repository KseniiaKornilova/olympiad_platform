from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import OlympiadUser, MultipleChoiceSubmission, OneChoiceSubmission, \
    TrueFalseSubmission, MultipleChoiceQuestion, OneChoiceQuestion, TrueFalseQuestion


@receiver(pre_delete, sender=OlympiadUser)
def pre_delete_dispatcher(sender, instance, **kwargs):
    MultipleChoiceSubmission.objects.filter(student=instance.user, question__olympiad=instance.olympiad).delete()
    OneChoiceSubmission.objects.filter(student=instance.user, question__olympiad=instance.olympiad).delete()
    TrueFalseSubmission.objects.filter(student=instance.user, question__olympiad=instance.olympiad).delete()


@receiver(post_save, sender=MultipleChoiceQuestion)
@receiver(post_save, sender=OneChoiceQuestion)
@receiver(post_save, sender=TrueFalseQuestion)
def post_save_dispatcher(sender, instance, **kwargs):
    olympiad = instance.olympiad
    olympiad.total_mark += instance.mark
    olympiad.save()