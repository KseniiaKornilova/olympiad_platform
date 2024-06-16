from django.contrib import admin
from .models import Olympiad, Subject, OlympiadUser, QuestionSection, Question, UserAnswer


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    fields = ('name',)
    list_display_links = ('name',)


class OlympiadUserInline(admin.TabularInline):
    model = OlympiadUser
    extra = 1


class OlympiadAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'degree')
    list_display_links = ('title',)
    search_fields = ('title', 'subject__name')
    list_per_page = 10
    list_filter = ('subject',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'subject', 'degree', 'stage', 'image'),
            'classes': ('wide',),
        }),
        ('Временные данные', {
            'fields': ('date_of_start', 'registration_dedline', 'olympiad_duration'),
            'classes': ('wide',),
        }),
    )
    inlines = (OlympiadUserInline,)


class QuestionSectionAdmin(admin.ModelAdmin):
    list_display = ('section', 'points')
    list_display_links = ('section',)
    search_fields = ('section',)
    fields = ('section', 'points')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_description', 'section', 'olympiad', 'correct_answer')
    list_display_links = ('question_description',)
    search_fields = ('question_description',)
    list_filter = ('olympiad',)
    fields = ('question_description', 'section', 'olympiad', 'correct_answer')


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'score')
    list_display_links = ('user',)
    search_fields = ('user__first_name', 'user__last_name', 'olympiad__title')


class OlympiadUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'olympiad', 'registration_date')
    list_display_links = ('user',)
    exclude = None
    search_fields = ('user__first_name', 'user__last_name')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Olympiad, OlympiadAdmin)
admin.site.register(QuestionSection, QuestionSectionAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
admin.site.register(OlympiadUser, OlympiadUserAdmin)
