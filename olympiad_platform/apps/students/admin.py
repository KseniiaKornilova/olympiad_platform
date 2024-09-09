from django.contrib import admin

from .models import User
from ..olympiads.models import OlympiadUser


class OlympiadInline(admin.TabularInline):
    model = OlympiadUser
    extra = 1


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'status', 'degree', 'degree_id', 'is_active')
    list_display_links = ('__str__',)
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('status',)
    list_per_page = 15
    fieldsets = (
        ('Основная информация', {
            'fields': ('last_name', 'first_name', 'patronymic', 'email', 'birthday', 'image'),
            'classes': ('wide',),
        }),
        ('Данные о школе', {
            'fields': ('status', ('degree', 'degree_id')),
            'classes': ('wide',),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=None)
        if obj:
            if obj.is_staff:
                fieldsets = (
                             ('Основная информация', {
                              'fields': ('last_name', 'first_name', 'patronymic', 'email', 'birthday', 'image'),
                              'classes': ('wide',),
                              }),
                )
        return fieldsets

    inlines = (OlympiadInline,)

    def get_inlines(self, request, obj=None):
        inlines = super().get_inlines(request, obj=None)
        if obj:
            if obj.is_staff:
                inlines = ()
        return inlines


admin.site.register(User, UserAdmin)
