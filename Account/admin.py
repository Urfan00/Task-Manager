from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Account, Department, UserStatus



class AccountAdmin(BaseUserAdmin):
    list_display = ('id', "email", "first_name", "last_name", 'FIN', "number", "image", "birthday", 'department', "is_active", "is_superuser")
    list_display_links = ('id', 'email')
    list_filter = ("is_active", 'is_staff', "is_superuser")
    fieldsets = (
        ("Credential", {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'number', 'bio', 'image', 'birthday')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
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
    ordering = ['email']  # Use a valid field from your model for ordering
    search_fields = ("first_name", "last_name", 'FIN', "email", "number", 'department__title')



class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']


class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_time_login', 'head_of_department', 'assistant', 'staff_department', 'account']
    search_fields = ['account__first_name', 'account__last_name', 'account__department__title']



admin.site.register(Account, AccountAdmin)
admin.site.register(UserStatus, UserStatusAdmin)
admin.site.register(Department, DepartmentAdmin)