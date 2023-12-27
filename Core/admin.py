from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import MemberTaskStatistic



class MemberTaskStatisticAdmin(ImportExportModelAdmin):
    list_display = ['id', 'member', 'sent_task_count', 'to_task_count', 'cc_task_count', 'forwarded_task_count', 'assigned_task_count', 'status', 'created_at', 'updated_at']
    list_display_links = ['id', 'member']
    search_fields = ['member__first_name', 'member__last_name']
    list_filter = ['status']

admin.site.register(MemberTaskStatistic, MemberTaskStatisticAdmin)
