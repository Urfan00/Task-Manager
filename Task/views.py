from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Task, TaskCCMembersAction, TaskToMembersAction
from .forms import TaskDetailForm, TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Case, When, Value, BooleanField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages



class InboxListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'inbox.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        to_task_search = self.request.GET.get('to_task_search', '')
        cc_task_search = self.request.GET.get('cc_task_search', '')

        to_tasks = Task.objects.order_by('-created_at').filter(
                task_to_member_action__to_member=self.request.user,
                task_to_member_action__task_member_is_pin = False,
                task_to_member_action__task_member_is_deleted = False,
                task_to_member_action__bin_deleted = False
            ).exclude(task_author=self.request.user).distinct().annotate(
            is_view=Case(
                When(task_to_member_action__to_member=self.request.user, task_to_member_action__task_member_is_read=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        to_tasks_pinned = Task.objects.order_by('-created_at').filter(
                task_to_member_action__to_member=self.request.user,
                task_to_member_action__task_member_is_pin = True,
                task_to_member_action__task_member_is_deleted = False,
                task_to_member_action__bin_deleted = False
            ).exclude(task_author=self.request.user).distinct().annotate(
            is_view=Case(
                When(task_to_member_action__to_member=self.request.user, task_to_member_action__task_member_is_read=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        cc_tasks = Task.objects.order_by('-created_at').filter(
            task_cc_member_action__cc_member=self.request.user,
            task_cc_member_action__task_member_is_pin = False,
            task_cc_member_action__task_member_is_deleted = False,
            task_cc_member_action__bin_deleted = False
        ).exclude(task_author=self.request.user).distinct().annotate(
            is_view=Case(
                When(task_cc_member_action__cc_member=self.request.user, task_cc_member_action__task_member_is_read=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        cc_tasks_pinned = Task.objects.order_by('-created_at').filter(
            task_cc_member_action__cc_member=self.request.user,
            task_cc_member_action__task_member_is_pin = True,
            task_cc_member_action__task_member_is_deleted = False,
            task_cc_member_action__bin_deleted = False
        ).exclude(task_author=self.request.user).distinct().annotate(
            is_view=Case(
                When(task_cc_member_action__cc_member=self.request.user, task_cc_member_action__task_member_is_read=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        if to_task_search:
            to_tasks = to_tasks.filter(
                 Q(task_title__icontains=to_task_search)
                 | Q(task_importance_level__icontains=to_task_search)
                 | Q(task_status__icontains=to_task_search)
                 | Q(task_author__first_name__icontains=to_task_search)
                 | Q(task_author__last_name__icontains=to_task_search)
                 | Q(task_author__department__title__icontains=to_task_search)
                 | Q(task_author__email__icontains=to_task_search)
                 | Q(task_author__status__icontains=to_task_search)
                 | Q(task_category__category_title__icontains=to_task_search)
                 )
            to_tasks_pinned = to_tasks_pinned.filter(
                 Q(task_title__icontains=to_task_search)
                 | Q(task_importance_level__icontains=to_task_search)
                 | Q(task_status__icontains=to_task_search)
                 | Q(task_author__first_name__icontains=to_task_search)
                 | Q(task_author__last_name__icontains=to_task_search)
                 | Q(task_author__department__title__icontains=to_task_search)
                 | Q(task_author__email__icontains=to_task_search)
                 | Q(task_author__status__icontains=to_task_search)
                 | Q(task_category__category_title__icontains=to_task_search)
                 )
        elif cc_task_search:
            cc_tasks = cc_tasks.filter(
                   Q(task_title__icontains=cc_task_search)
                 | Q(task_importance_level__icontains=cc_task_search)
                 | Q(task_status__icontains=cc_task_search)
                 | Q(task_author__first_name__icontains=cc_task_search)
                 | Q(task_author__last_name__icontains=cc_task_search)
                 | Q(task_author__department__title__icontains=cc_task_search)
                 | Q(task_author__email__icontains=cc_task_search)
                 | Q(task_author__status__icontains=cc_task_search)
                 | Q(task_category__category_title__icontains=cc_task_search)
            )
            cc_tasks_pinned = cc_tasks_pinned.filter(
                   Q(task_title__icontains=cc_task_search)
                 | Q(task_importance_level__icontains=cc_task_search)
                 | Q(task_status__icontains=cc_task_search)
                 | Q(task_author__first_name__icontains=cc_task_search)
                 | Q(task_author__last_name__icontains=cc_task_search)
                 | Q(task_author__department__title__icontains=cc_task_search)
                 | Q(task_author__email__icontains=cc_task_search)
                 | Q(task_author__status__icontains=cc_task_search)
                 | Q(task_category__category_title__icontains=cc_task_search)
            )

        # Pagination to_tasks
        to_task_search_page = self.request.GET.get('to_task_search_page')
        paginator = Paginator(to_tasks, self.paginate_by)

        try:
            to_tasks = paginator.page(to_task_search_page)
        except PageNotAnInteger:
            to_tasks = paginator.page(1)
        except EmptyPage:
            to_tasks = paginator.page(paginator.num_pages)

        # Pagination cc_tasks
        cc_task_search_page = self.request.GET.get('cc_task_search_page')
        paginator = Paginator(cc_tasks, self.paginate_by)

        try:
            cc_tasks = paginator.page(cc_task_search_page)
        except PageNotAnInteger:
            cc_tasks = paginator.page(1)
        except EmptyPage:
            cc_tasks = paginator.page(paginator.num_pages)


        context['to_tasks'] = to_tasks
        context['cc_tasks'] = cc_tasks
        context['to_tasks_pinned'] = to_tasks_pinned
        context['cc_tasks_pinned'] = cc_tasks_pinned

        return context


class SendTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'send_task.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(task_author=self.request.user, task_author_is_deleted=False, bin_deleted=False).order_by('-created_at').all()

        search = self.request.GET.get('search', '')


        if search:
            tasks = tasks.filter(
                 Q(task_title__icontains=search)
                 | Q(task_importance_level__icontains=search)
                 | Q(task_status__icontains=search)
                 | Q(task_author__first_name__icontains=search)
                 | Q(task_author__last_name__icontains=search)
                 | Q(task_author__department__title__icontains=search)
                 | Q(task_author__email__icontains=search)
                 | Q(task_author__status__icontains=search)
                 | Q(task_category__category_title__icontains=search)
                 )

        # Pagination cc_tasks
        page = self.request.GET.get('page')
        paginator = Paginator(tasks, self.paginate_by)

        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        context["tasks"] = tasks

        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('create')

    def form_valid(self, form):
        # Set the task_author to the current user before saving
        form.instance.task_author = self.request.user
        messages.success(self.request, 'Task successfully send.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Additional logic can be added here if needed
        messages.error(self.request, 'Could not send the task')
        return super().form_invalid(form)


class BinListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'bin.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search = self.request.GET.get('search', '')


        bin_tasks = Task.objects.filter(
              Q(task_author=self.request.user, task_author_is_deleted=True, bin_deleted=False)
            | Q(task_to_member_action__to_member=self.request.user, task_to_member_action__task_member_is_deleted=True, task_to_member_action__bin_deleted=False)
            | Q(task_cc_member_action__cc_member=self.request.user, task_cc_member_action__task_member_is_deleted=True, task_cc_member_action__bin_deleted=False)
        ).order_by('-created_at').distinct()

        if search:
            bin_tasks = bin_tasks.filter(
                 Q(task_title__icontains=search)
                 | Q(task_importance_level__icontains=search)
                 | Q(task_status__icontains=search)
                 | Q(task_author__first_name__icontains=search)
                 | Q(task_author__last_name__icontains=search)
                 | Q(task_author__department__title__icontains=search)
                 | Q(task_author__email__icontains=search)
                 | Q(task_author__status__icontains=search)
                 | Q(task_category__category_title__icontains=search)
                 )

        # Pagination to_tasks
        page = self.request.GET.get('page')
        paginator = Paginator(bin_tasks, self.paginate_by)

        try:
            bin_tasks = paginator.page(page)
        except PageNotAnInteger:
            bin_tasks = paginator.page(1)
        except EmptyPage:
            bin_tasks = paginator.page(paginator.num_pages)

        context["bin_tasks"] = bin_tasks
        return context


class TaskDetailView(LoginRequiredMixin, DetailView, CreateView):
    model = Task
    template_name = 'task-detail.html'
    form_class = TaskDetailForm
    context_object_name = 'editTask'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['to_members_actions'] = TaskToMembersAction.objects.filter(task=self.object)
        context['cc_members_actions'] = TaskCCMembersAction.objects.filter(task=self.object)
        return context

    def form_valid(self, form, *args, **kwargs):
        # Get the task instance
        task = Task.objects.get(pk=self.kwargs.get('pk'))

        # Update the task_status field with the form data
        task.task_status = form.cleaned_data['task_status']

        # Save the updated instance
        task.save()
        messages.success(self.request, 'Task status successfully change.')

        return redirect("task_detail", pk=self.kwargs.get('pk'))

# PIN & DELETE & UNDELETE & DELETE FOREVER
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def toggle_action_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        action_type = request.POST.get('action_type')
        
        # Use get_object_or_404 to handle the case where the Task doesn't exist
        task = get_object_or_404(Task, id=task_id)
        
        # Check if the task_to_member_action and task_cc_member_action exist
        pin_delete_to_member = task.task_to_member_action.filter(task=task, to_member=request.user).first()
        pin_delete_cc_member = task.task_cc_member_action.filter(task=task, cc_member=request.user).first()
        pin_delete_send_member = Task.objects.filter(id=task_id, task_author=request.user).first()

        if action_type == 'pin':
            # Toggle the task_member_is_pin status for task_to_member_action
            if pin_delete_to_member:
                pin_delete_to_member.task_member_is_pin = not pin_delete_to_member.task_member_is_pin
                pin_delete_to_member.save()

            # Toggle the task_member_is_pin status for task_cc_member_action
            if pin_delete_cc_member:
                pin_delete_cc_member.task_member_is_pin = not pin_delete_cc_member.task_member_is_pin
                pin_delete_cc_member.save()

            return JsonResponse({'is_pinned': pin_delete_to_member.task_member_is_pin if pin_delete_to_member else False})

        elif action_type == 'delete':
            # Set the task_member_is_deleted status to True for task_to_member_action
            if pin_delete_to_member:
                pin_delete_to_member.task_member_is_deleted = True
                pin_delete_to_member.save()

            # Set the task_member_is_deleted status to True for task_cc_member_action
            if pin_delete_cc_member:
                pin_delete_cc_member.task_member_is_deleted = True
                pin_delete_cc_member.save()

            if pin_delete_send_member:
                pin_delete_send_member.task_author_is_deleted = True
                pin_delete_send_member.save()

            return JsonResponse({'is_deleted': pin_delete_to_member.task_member_is_deleted if pin_delete_to_member else False})

        elif action_type == 'undelete':
            # Set the task_member_is_deleted status to False for task_to_member_action
            if pin_delete_to_member:
                pin_delete_to_member.task_member_is_deleted = False
                pin_delete_to_member.save()

            # Set the task_member_is_deleted status to False for task_cc_member_action
            if pin_delete_cc_member:
                pin_delete_cc_member.task_member_is_deleted = False
                pin_delete_cc_member.save()

            if pin_delete_send_member:
                pin_delete_send_member.task_author_is_deleted = False
                pin_delete_send_member.save()

            return JsonResponse({'is_deleted': pin_delete_to_member.task_member_is_deleted if pin_delete_to_member else False})

        elif action_type == 'delete_forever':
            # Set the bin_deleted status to True for task_to_member_action
            if pin_delete_to_member:
                pin_delete_to_member.bin_deleted = True
                pin_delete_to_member.save()

            # Set the bin_deleted status to True for task_cc_member_action
            if pin_delete_cc_member:
                pin_delete_cc_member.bin_deleted = True
                pin_delete_cc_member.save()

            if pin_delete_send_member:
                pin_delete_send_member.bin_deleted = True
                pin_delete_send_member.save()

            return JsonResponse({'deleted': True})
