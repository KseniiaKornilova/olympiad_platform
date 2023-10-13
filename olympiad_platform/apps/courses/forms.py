from django import forms
from .models import Comment


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

    # def __init__(self, *args, **kwargs):
    #     super(UserCommentForm, self).__init__(*args, **kwargs)
    #     self.fields['course'].required = False
    #     self.fields['lesson'].required = False







