from django.contrib import admin

from .models import MultipleChoiceQuestion, MultipleChoiceSubmission, Olympiad, OlympiadUser, OneChoiceQuestion, \
    OneChoiceSubmission, Subject, TrueFalseQuestion, TrueFalseSubmission


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
            'fields': ('title', 'subject', 'description', 'degree', 'stage', 'image'),
            'classes': ('wide',),
        }),
        ('Временные данные', {
            'fields': ('date_of_start', 'registration_dedline'),
            'classes': ('wide',),
        }),
    )
    inlines = (OlympiadUserInline,)


class OlympiadUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'olympiad', 'registration_date')
    list_display_links = ('user',)
    exclude = None
    search_fields = ('user__first_name', 'user__last_name')


class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_num', 'olympiad')
    ordering = ('question_num',)
    list_display_links = ('title',)
    search_fields = ('olympiad__title', 'assignment__title')
    fieldsets = (
        ('Основная информация', {
            'fields': ('question_num', 'title', 'description', 'mark', 'olympiad'),
            'classes': ('wide',),
        }),
        ('Варианты ответов', {
            'fields': ('a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct', 'e',
                       'e_is_correct', 'f', 'f_is_correct'),
            'classes': ('wide',),
        }),
    )


class MultipleChoiceSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'students_mark')
    ordering = ('student',)
    list_display_links = ('student',)
    search_fields = ('student__first_name', 'student__last_name')
    fieldsets = (
        ('Основная информация', {
            'fields': ('student', 'question', 'students_mark'),
            'classes': ('wide',),
        }),
        ('Варианты ответов', {
            'fields': ('a', 'b', 'c', 'd', 'e', 'f'),
            'classes': ('wide',),
        }),
    )


class OneChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_num', 'olympiad')
    ordering = ('question_num',)
    list_display_links = ('title',)
    search_fields = ('olympiad__title', 'assignment__title')
    fieldsets = (
        ('Основная информация', {
            'fields': ('question_num', 'title', 'description', 'mark', 'olympiad'),
            'classes': ('wide',),
        }),
        ('Варианты ответов', {
            'fields': ('a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct'),
            'classes': ('wide',),
        }),
    )


class OneChoiceSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'students_mark')
    ordering = ('student',)
    list_display_links = ('student',)
    search_fields = ('student__first_name', 'student__last_name')
    fieldsets = (
        ('Основная информация', {
            'fields': ('student', 'question', 'students_mark'),
            'classes': ('wide',),
        }),
        ('Варианты ответов', {
            'fields': ('a', 'b', 'c', 'd'),
            'classes': ('wide',),
        }),
    )


class TrueFalseQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_num', 'olympiad')
    list_display_links = ('title',)
    search_fields = ('olympiad__title', 'assignment__title')
    fieldsets = (
        ('Основная информация', {
            'fields': ('question_num', 'title', 'description', 'mark', 'olympiad'),
            'classes': ('wide',),
        }),
        ('Варианты ответов', {
            'fields': ('first_statement', 'second_statement', 'answer'),
            'classes': ('wide',),
        }),
    )


class TrueFalseSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'students_mark')
    ordering = ('student',)
    list_display_links = ('student',)
    search_fields = ('student__first_name', 'student__last_name')
    fields = ('student', 'question', 'students_mark', 'answer')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Olympiad, OlympiadAdmin)
admin.site.register(OlympiadUser, OlympiadUserAdmin)
admin.site.register(OneChoiceQuestion, OneChoiceQuestionAdmin)
admin.site.register(OneChoiceSubmission, OneChoiceSubmissionAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(MultipleChoiceSubmission, MultipleChoiceSubmissionAdmin)
admin.site.register(TrueFalseQuestion, TrueFalseQuestionAdmin)
admin.site.register(TrueFalseSubmission, TrueFalseSubmissionAdmin)
