from django.contrib import admin
from .models import Course, CourseUser, Lesson, Assignment, AssignmentSubmission, MultipleChoiceQuestion, MultipleChoiceSubmission, OneChoiceQuestion, OneChoiceSubmission, TrueFalseQuestion, TrueFalseSubmission, Comment

# Register your models here.
class CourseUserInline(admin.TabularInline):
    model = CourseUser
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    list_display_links = ('title',)
    search_fields = ('^title', '^subject')
    list_per_page = 10
    list_filter = ('subject',)
    fields = ('title', 'subject', 'course_description', 'category', 'month_amount', 'times_a_week', 'price','teacher', 'image')

    inlines = (CourseUserInline,)
    autocomplete_fields = ('participants',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'course')
    list_display_links = ('title',)
    search_fields = ('^title', 'number')
    list_per_page = 10
    list_filter = ('course',)
    fields = ('number', 'title', 'course')


class CourseUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'earned_mark', 'percent_mark')
    list_display_links = ('user',)
    search_fields = ('^user', '^course')
    list_filter = ('course',)
    fields = ('user', 'course', 'is_finished', 'earned_mark')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assignment_num')
    list_display_links = ('title',)
    search_fields = ('^title', '^course')
    list_filter = ('course',)
    fields = ('assignment_num', 'title', 'description', 'course', 'total_mark', 'image')


class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'earned_mark', 'homework_file')
    list_display_links = ('assignment',)
    search_fields = ('^assignment', '^student')
    list_filter = ('student',)
    fields = ('assignment', 'student', 'earned_mark', 'is_finished', 'homework_file')


class MultipleChoiceQuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question_num', 'olympiad', 'assignment')
    ordering = ('question_num',)
    list_display_links = ('title',)
    search_fields = ('^olympiad', '^assignment')
    fieldsets = (
        ('Основная информация', {
            'fields': ('question_num', 'title', 'description', 'mark', 'olympiad', 'assignment'),
            'classes': ('wide',),
        }),
        ('Варианты ответов', {
            'fields': ('a', 'a_is_correct', 'b', 'b_is_correct', 'c', 'c_is_correct', 'd', 'd_is_correct', 'e', 'e_is_correct', 'f', 'f_is_correct'),
            'classes': ('wide',),
        }),
    )


class MultipleChoiceSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'students_mark')
    ordering = ('student',)
    list_display_links = ('student',)
    search_fields = ('^student',)
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
    list_display = ('title', 'question_num', 'olympiad', 'assignment')
    ordering = ('question_num',)
    list_display_links = ('title',)
    search_fields = ('^olympiad', '^assignment')
    fieldsets = (
        ('Основная информация', {
            'fields': ('question_num', 'title', 'description', 'mark', 'olympiad', 'assignment'),
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
    search_fields = ('^student',)
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
    list_display = ('title', 'question_num', 'assignment', 'olympiad')
    list_display_links = ('title',)
    search_fields = ('^assignment', '^olympiad')
    fieldsets = (
        ('Основная информация', {
            'fields': ('question_num', 'title', 'description', 'marks', 'olympiad', 'assignment'),
            'classes': ('wide',),
        }),
        ('Варианты ответов', {
            'fields': ('true_choice', 'false_choice', 'answer'),
            'classes': ('wide',),
        }),
    )


class TrueFalseSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'students_mark')
    ordering = ('student',)
    list_display_links = ('student',)
    search_fields = ('^student',)
    fields = ('student', 'question', 'students_mark', 'answer')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'student', 'content')
    ordering = ('lesson',)
    list_display_links = ('lesson',)
    exclude = None
       


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseUser, CourseUserAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(AssignmentSubmission, AssignmentSubmissionAdmin)
admin.site.register(MultipleChoiceQuestion, MultipleChoiceQuestionAdmin)
admin.site.register(MultipleChoiceSubmission, MultipleChoiceSubmissionAdmin)
admin.site.register(OneChoiceQuestion, OneChoiceQuestionAdmin)
admin.site.register(OneChoiceSubmission, OneChoiceSubmissionAdmin)
admin.site.register(TrueFalseQuestion, TrueFalseQuestionAdmin)
admin.site.register(TrueFalseSubmission, TrueFalseSubmissionAdmin)
admin.site.register(Comment, CommentAdmin)
