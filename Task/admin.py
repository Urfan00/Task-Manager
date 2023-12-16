from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Task



class TaskAdmin(ImportExportModelAdmin):
    list_display = ['id', 'task_title', 'task_image', 'task_author', 'task_status', 'task_deadline', 'task_is_flag', 'task_is_read', 'task_is_pin', 'task_is_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'task_title']
    search_fields = ['title', 'task_author__first_name', 'task_author__last_name']
    list_filter = ['task_is_flag', 'task_is_read', 'task_is_pin', 'task_is_deleted']


admin.site.register(Task, TaskAdmin)


