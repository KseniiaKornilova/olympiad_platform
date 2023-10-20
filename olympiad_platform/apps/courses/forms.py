from django import forms
from django.core.validators import FileExtensionValidator
from .models import Comment, AssignmentSubmission


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ()
        widgets = {"course": forms.HiddenInput(attrs={
                    'class': 'form-control form-group mb-3'
                    }),
                    "lesson": forms.HiddenInput(attrs={
                    'class': 'form-control form-group mb-3'
                    }),
                    "student": forms.TextInput(attrs={
                        'class': 'form-control form-group mb-3',
                        'placeholder': 'Автор комментария',
                        'readonly': 'readonly'
                    }),
                    "content": forms.TextInput(attrs={
                        'class': 'form-control form-group mb-3',
                        'placeholder': 'Текст комментария'
                    }),
                    "created_at": forms.DateInput(attrs={
                        'class': 'form-control form-group mb-3',
                        'placeholder': 'Дата отправки комментария'
                    })
            }



class AssignmentSubmissionForm(forms.ModelForm):
    homework_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control form-group mb-3'}),
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'], message='Пожалуйста, прикрепите файл с расширением .pdf или .doc')]
        )
        
    class Meta:
        model = AssignmentSubmission
        fields = ['homework_file']
        








