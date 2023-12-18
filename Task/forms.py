from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Task, TaskCategory, TaskToMembersAction, TaskCCMembersAction
from ckeditor.widgets import CKEditorWidget
from Account.models import Account


class TaskForm(forms.ModelForm):
    to_member = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        widget=FilteredSelectMultiple("To members", is_stacked=False),
        required=False
    )

    cc_member = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        widget=FilteredSelectMultiple("CC members", is_stacked=False),
        required=False
    )

    task_category = forms.ModelChoiceField(
        queryset=TaskCategory.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'task_title',
            'task_image',
            'task_content',
            'task_status',
            'task_importance_level',
            'task_deadline',
            'task_category'
        ]
        widgets = {
            'task_content': CKEditorWidget(),
        }

    def save(self, commit=True):
        task = super().save(commit)
        
        to_members = self.cleaned_data.get('to_member', [])
        cc_members = self.cleaned_data.get('cc_member', [])

        for tmember in to_members:
            TaskToMembersAction.objects.create(task=task, to_member=tmember)

        for cmember in cc_members:
            TaskCCMembersAction.objects.create(task=task, cc_member=cmember)

        return task
