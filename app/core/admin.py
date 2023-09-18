from django.contrib import admin
from .models import User
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.db import models
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.decorators import action, display
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django.contrib.auth.models import Group


admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(Group)


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(ModelAdmin):
    pass


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(ModelAdmin):
    pass



@admin.register(User)
class UserAdminModel(BaseUserAdmin, ModelAdmin):
    list_display = [
        "display_header",
        "user_type",
        "is_active",
        "display_staff",
        "display_superuser",
        "display_created",
    ]
    list_editable = ['is_active']
    readonly_fields = ['last_login']
    list_per_page = 20
    search_fields = ['username', "first_name", "last_name", "email"]
    date_hierarchy = 'date_joined'
    empty_value_display = '-empty-'
    list_filter = ['user_type']
    save_as_continue = False
    show_full_result_count = True
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    readonly_fields = ["last_login", "updated_at", "date_joined"]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('username', 'email','password1', 'password2'), )
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': (('first_name','last_name'), ('other_name', 'contact'), 'user_type', ),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser',  ),
        }),
        ('Account Status',{
            'classes': ('wide'),
            'fields': ['is_verified']
        }),
        ('Groups', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', ),
        }),
        ("Important dates", {
            'classes': ('wide',),
            "fields": ("last_login", "updated_at", "date_joined")
        }),
    )
    fieldsets = (
        ('Account Information', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', )
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': (('first_name', 'last_name','other_name', 'contact'), 'user_type', ),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', ),
        }),
        ('Account Status', {
            'classes': ('wide'),
            'fields': ['is_verified']
        }),
        ('Groups', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', ),
        }),
        (("Important dates"), {
            'classes': ('wide',),
            "fields": ("last_login", "updated_at", "date_joined")
        }),
    )

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @display(description=_("User"), header=True)
    def display_header(self, instance: User):
        return instance.name, instance.email

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

    @display(description=_("Created"))
    def display_created(self, instance: User):
        return instance.date_joined


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
