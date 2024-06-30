from django.contrib import admin
from .models import Course, CourseUser, Lesson, Assignment, AssignmentSubmission, Comment


class CourseUserInline(admin.TabularInline):
    model = CourseUser
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    list_display_links = ('title',)
    search_fields = ('title', 'subject__name')
    list_per_page = 10
    list_filter = ('subject',)
    fields = ('title', 'subject', 'course_description', 'category', 'month_amount', 'times_a_week', 'price', 
              'teacher', 'image')

    inlines = (CourseUserInline,)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'course')
    list_display_links = ('title',)
    search_fields = ('title', 'number')
    list_per_page = 10
    list_filter = ('course',)
    fields = ('number', 'title', 'course', 'content')


class CourseUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'earned_mark', 'percent_mark')
    list_display_links = ('user',)
    search_fields = ('user__last_name', 'user__first_name', 'course__title')
    list_filter = ('course',)
    fields = ('user', 'course', 'is_finished', 'earned_mark')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'assignment_num')
    list_display_links = ('title',)
    search_fields = ('title', 'course__title')
    list_filter = ('course',)
    fields = ('assignment_num', 'title', 'description', 'course', 'total_mark', 'image')


class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'earned_mark', 'homework_file')
    list_display_links = ('assignment',)
    search_fields = ('assignment__title', 'student__first_name', 'user__last_name')
    list_filter = ('student',)
    fields = ('assignment', 'student', 'earned_mark', 'status', 'is_finished', 'homework_file')


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
admin.site.register(Comment, CommentAdmin)
