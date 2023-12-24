from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account, Department
from import_export.admin import ImportExportModelAdmin



class AccountAdmin(BaseUserAdmin, ImportExportModelAdmin):
    list_display = ('id', "email", "first_name", "last_name", 'FIN', "number", "image", "birthday", 'department', 'status', 'first_time_login', "is_active", "is_superuser")
    list_display_links = ('id', 'email')
    list_filter = ("is_active", 'is_staff', "is_superuser", 'first_time_login')
    fieldsets = (
        ("Credential", {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio', 'FIN', "number", "image", "birthday", 'department', 'status')}),
        ('Permissions', {
            'fields': ('first_time_login', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            'CREATE NEW USER',
            {
                "classes": ("wide",),
                "fields": ("password1", "password2", "first_name", "last_name", 'FIN', "email", "number"),
            },
        ),
    )
    ordering = ['id']  # Use a valid field from your model for ordering
    search_fields = ("first_name", "last_name", 'FIN', "email", "number", 'department__title')


class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']



admin.site.register(Account, AccountAdmin)
admin.site.register(Department, DepartmentAdmin)
