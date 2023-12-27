from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ForwardTask, ForwardedToWhom, Task, TaskActionLog, TaskCategory, TaskToMembersAction, TaskCCMembersAction



class TaskCategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'category_title', 'created_at', 'updated_at']
    list_display_links = ['id', 'category_title']
    search_fields = ['category_title']


class TaskAdmin(ImportExportModelAdmin):
    list_display = ['id', 'task_title', 'task_image', 'task_author', 'task_category', 'task_status', 'task_importance_level', 'task_deadline', 'task_author_is_deleted', 'bin_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'task_title']
    search_fields = ['task_title', 'task_author__first_name', 'task_author__last_name', 'task_category__category_title']
    list_filter = ['task_author_is_deleted', 'bin_deleted']


class TaskToMembersActionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'to_member', 'task', 'task_member_is_read', 'task_member_is_pin', 'task_member_is_deleted', 'bin_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'to_member']
    search_fields = ['task__task_title', 'to_member__first_name', 'to_member__last_name']
    list_filter = ['task_member_is_read', 'task_member_is_pin', 'task_member_is_deleted', 'bin_deleted']


class TaskCCMembersActionAdmin(ImportExportModelAdmin):
    list_display = ['id', 'cc_member', 'task', 'task_member_is_read', 'task_member_is_pin', 'task_member_is_deleted', 'bin_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'cc_member']
    search_fields = ['task__task_title', 'cc_member__first_name', 'cc_member__last_name']
    list_filter = ['task_member_is_read', 'task_member_is_pin', 'task_member_is_deleted', 'bin_deleted']


class TaskActionLogAdmin(ImportExportModelAdmin):
    list_display = ['id', 'log_author', 'task', 'old_status', 'new_status', 'created_at', 'updated_at']
    list_display_links = ['id', 'log_author']
    search_fields = ['log_author__first_name', 'log_author__last_name']


class ForwardTaskAdmin(ImportExportModelAdmin):
    list_display = ['id', 'forward_author', 'task', 'forward_author_task_is_deleted', 'bin_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'forward_author']
    search_fields = ['forward_author__first_name', 'forward_author__last_name', 'task__task_title']
    list_filter = ['forward_author_task_is_deleted', 'bin_deleted']


class ForwardedToWhomAdmin(ImportExportModelAdmin):
    list_display = ['id', 'whom', 'forward_task', 'whom_is_read', 'whom_is_pin', 'whom_is_deleted', 'bin_deleted', 'created_at', 'updated_at']
    list_display_links = ['id', 'whom']
    search_fields = ['whom__first_name', 'whom__last_name', 'forward_task__task__task_title']
    list_filter = ['whom_is_read', 'whom_is_pin', 'whom_is_deleted', 'bin_deleted']



admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCategory, TaskCategoryAdmin)
admin.site.register(TaskToMembersAction, TaskToMembersActionAdmin)
admin.site.register(TaskCCMembersAction, TaskCCMembersActionAdmin)
admin.site.register(TaskActionLog, TaskActionLogAdmin)
admin.site.register(ForwardTask, ForwardTaskAdmin)
admin.site.register(ForwardedToWhom, ForwardedToWhomAdmin)
