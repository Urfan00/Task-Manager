from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import ForwardTask, ForwardedToWhom, Task, TaskCategory, TaskToMembersAction, TaskCCMembersAction
from ckeditor.widgets import CKEditorWidget
from Account.models import Account
from django.db.models import Q


class TaskForm(forms.ModelForm):
    to_member = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        # widget=FilteredSelectMultiple("To members", is_stacked=False, attrs={'class': 'form-control'}),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    cc_member = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        # widget=FilteredSelectMultiple("CC members", is_stacked=False, attrs={'class': 'form-control'}),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    task_category = forms.ModelChoiceField(
        queryset=TaskCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    # Other fields and Meta class remain unchanged...

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if user:
            # Adjust the to_member and cc_member field queryset based on the user's role
            if user.status == 'Head of Department':
                # Head of Department can send tasks to anyone
                self.fields['to_member'].queryset = Account.objects.exclude(id=user.id)
                self.fields['cc_member'].queryset = Account.objects.exclude(id=user.id)

            elif user.status == 'Assistant':
                # Assistant can send tasks to everyone except Head of Department
                self.fields['to_member'].queryset = Account.objects.exclude(Q(status='Head of Department') | Q(id=user.id))
                self.fields['cc_member'].queryset = Account.objects.exclude(id=user.id)

            elif user.status == 'Staff Department':
                # Staff Department can send tasks and cc_member to other staff members
                self.fields['to_member'].queryset = Account.objects.exclude(Q(status='Head of Department')| Q(status='Assistant') | Q(id=user.id))
                self.fields['cc_member'].queryset = Account.objects.exclude(id=user.id)

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
            'task_title' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'type' : 'text'
                }
            ),
            'task_image' : forms.ClearableFileInput(
                attrs={
                    'type' : 'file',
                    'class' : 'form-control',
                }
            ),
            'task_status' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-",
                    'class' : 'form-control',

                }
            ),
            'task_category' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-",
                    'class' : 'form-control',

                }
            ),
            'task_importance_level' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-",
                    'class' : 'form-control',

                }
            ),
            'task_deadline' : forms.DateTimeInput(
                attrs={
                    "class" : 'inpClass form-control',
                    'type': 'datetime-local',
                    'placeholder' :"yyyy-dd-mm"
                }
            )
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


class TaskDetailForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_status']
        widgets = {
            'task_status' : forms.Select(
                attrs={
                    'placeholder' :"-seçin-",
                    'class' : 'form-control',

                }
            )
        }


class ForwardForm(forms.ModelForm):
    whom = forms.ModelMultipleChoiceField(
        queryset=Account.objects.all(),
        # widget=FilteredSelectMultiple("Members", is_stacked=False, attrs={'class': 'form-control'}),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ForwardForm, self).__init__(*args, **kwargs)

        if user:
            # Adjust the to_member and cc_member field queryset based on the user's role
            if user.status == 'Head of Department':
                # Head of Department can send tasks to anyone
                self.fields['whom'].queryset = Account.objects.exclude(id=user.id)

            elif user.status == 'Assistant':
                # Assistant can send tasks to everyone except Head of Department
                self.fields['whom'].queryset = Account.objects.exclude(Q(status='Head of Department') | Q(id=user.id))

            elif user.status == 'Staff Department':
                # Staff Department can send tasks and cc_member to other staff members
                self.fields['whom'].queryset = Account.objects.exclude(Q(status='Head of Department')| Q(status='Assistant') | Q(id=user.id))

    class Meta:
        model = ForwardTask
        fields = ['forward_author_content']
        widgets = {
            'forward_author_content': CKEditorWidget()
            }

    def save(self, commit=True):
        forward_task = super().save(commit)
        
        whom = self.cleaned_data.get('whom', [])

        for member in whom:
            ForwardedToWhom.objects.create(forward_task=forward_task, whom=member)

        return forward_task
