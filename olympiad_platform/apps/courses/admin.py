from django.contrib import admin
from .models import Course, CourseUser, Lesson

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
    fields = ('title', 'subject', 'course_description', 'month_amount', 'times_a_week', 'image')

    inlines = (CourseUserInline,)
    autocomplete_fields = ('participants',)


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'course')
    list_display_links = ('title',)
    search_fields = ('^title', 'number')
    list_per_page = 10
    list_filter = ('course',)
    fields = ('number', 'title', 'course')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
