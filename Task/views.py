from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from Core.models import MemberTaskStatistic
from .models import ForwardTask, ForwardedToWhom, Task, TaskActionLog, TaskCCMembersAction, TaskToMembersAction
from .forms import ForwardForm, TaskDetailForm, TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q, Case, When, Value, BooleanField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime


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

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        # Set the task_author to the current user before saving
        form.instance.task_author = self.request.user

        try:
            member_statistic = MemberTaskStatistic.objects.get(member=self.request.user, status=True)
        except MemberTaskStatistic.DoesNotExist:
            member_statistic = None

        if member_statistic:
            if  member_statistic.created_at.date() != datetime.now().date():
                member_statistic.status = False
                MemberTaskStatistic.objects.create(
                    member=self.request.user,
                    sent_task_count=1,
                    to_task_count=form.cleaned_data['to_member'].count(),
                    cc_task_count=form.cleaned_data['cc_member'].count()
                )
            else:
                member_statistic.sent_task_count += 1
                member_statistic.to_task_count += form.cleaned_data['to_member'].count()
                member_statistic.cc_task_count += form.cleaned_data['cc_member'].count()

            member_statistic.save()
        else:
            MemberTaskStatistic.objects.create(
                    member=self.request.user,
                    sent_task_count=1,
                    to_task_count=form.cleaned_data['to_member'].count(),
                    cc_task_count=form.cleaned_data['cc_member'].count()
                )


        messages.success(self.request, 'Task successfully sent.')
        return super().form_valid(form)

    def form_invalid(self, form):
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
            Q(task_author=self.request.user, task_author_is_deleted=True, bin_deleted=False) |
            Q(task_to_member_action__to_member=self.request.user, task_to_member_action__task_member_is_deleted=True, task_to_member_action__bin_deleted=False) |
            Q(task_cc_member_action__cc_member=self.request.user, task_cc_member_action__task_member_is_deleted=True, task_cc_member_action__bin_deleted=False) |
            Q(task_forward__forward_author=self.request.user, task_forward__forward_author_task_is_deleted=True, task_forward__bin_deleted=False) |
            Q(task_forward__forward_task__whom=self.request.user, task_forward__forward_task__whom_is_deleted=True, task_forward__forward_task__bin_deleted=False)
        ).order_by('-created_at').distinct()

        bin_tasks = bin_tasks.annotate(
            forward_task_id=F('task_forward__id'),
            assigned_task_id=F('task_forward__forward_task__id'))

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
        context['logs'] = TaskActionLog.objects.filter(task=self.object).order_by('-created_at').all()[:5]

        # Mark the task as read for the current user (assuming the current user is either to_member or cc_member)

        to_member_action = TaskToMembersAction.objects.filter(task=self.object, to_member=self.request.user).first()
        cc_member_action = TaskCCMembersAction.objects.filter(task=self.object, cc_member=self.request.user).first()
        assigned_task_read = ForwardedToWhom.objects.filter(forward_task__task=self.object, whom=self.request.user).first()

        if to_member_action:
            to_member_action.task_member_is_read = True
            to_member_action.save()

        if cc_member_action:
            cc_member_action.task_member_is_read = True
            cc_member_action.save()

        if assigned_task_read:
            assigned_task_read.whom_is_read = True
            assigned_task_read.save()

        return context

    def form_valid(self, form, *args, **kwargs):
        # Get the task instance
        task = Task.objects.get(pk=self.kwargs.get('pk'))
        old_status = task.task_status

        task.task_status = form.cleaned_data['task_status']
        task.save()

        # Create a TaskActionLog entry for the status change
        TaskActionLog.objects.create(
            log_author=self.request.user,
            task=task,
            old_status=old_status,
            new_status=task.task_status,
        )

        messages.success(self.request, 'Task status successfully changed.')

        return redirect("task_detail", pk=self.kwargs.get('pk'))


# Forwarded Task
class ForwardTaskListView(LoginRequiredMixin, ListView):
    model = ForwardTask
    template_name = 'forward/forward.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        forwarded_tasks = ForwardTask.objects.filter(
            forward_author=self.request.user,
            forward_author_task_is_deleted=False,
            bin_deleted=False).order_by('-created_at').all()

        search = self.request.GET.get('search', '')

        if search:
            forwarded_tasks = forwarded_tasks.filter(
                Q(task__task_title__icontains=search) |
                Q(task__task_category__category_title__icontains=search) |
                Q(task__task_status__icontains=search) |
                Q(task__task_importance_level__icontains=search)
                # Q(forward_task__whom__first_name__icontains= search) |
                # Q(forward_task__whom__last_name__icontains= search)
            )

        # Pagination cc_tasks
        page = self.request.GET.get('page')
        paginator = Paginator(forwarded_tasks, self.paginate_by)

        try:
            forwarded_tasks = paginator.page(page)
        except PageNotAnInteger:
            forwarded_tasks = paginator.page(1)
        except EmptyPage:
            forwarded_tasks = paginator.page(paginator.num_pages)

        context["forwarded_tasks"] = forwarded_tasks

        return context


class AssignedTaskListView(LoginRequiredMixin, ListView):
    model = ForwardedToWhom
    template_name = 'forward/assigned.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        assigned_tasks = ForwardedToWhom.objects.filter(
            whom=self.request.user,
            whom_is_deleted=False,
            whom_is_pin=False,
            bin_deleted=False).order_by('-created_at').all()

        assigned_tasks_pinned = ForwardedToWhom.objects.filter(
            whom=self.request.user,
            whom_is_deleted=False,
            whom_is_pin=True,
            bin_deleted=False).order_by('-created_at').all()

        search = self.request.GET.get('search', '')

        if search:
            assigned_tasks = assigned_tasks.filter(
                Q(forward_task__task__task_author__first_name__icontains=search) |
                Q(forward_task__task__task_author__last_name__icontains=search) |
                Q(forward_task__task__task_author__email__icontains=search) |
                Q(forward_task__task__task_author__department__title__icontains=search) |
                Q(forward_task__task__task_author__status__icontains=search) |
                Q(forward_task__task__task_author__status__icontains=search) |
                Q(forward_task__forward_author__first_name__icontains=search) |
                Q(forward_task__forward_author__last_name__icontains=search) |
                Q(forward_task__forward_author__email__icontains=search) |
                Q(forward_task__forward_author__department__title__icontains=search) |
                Q(forward_task__forward_author__status__icontains=search) |
                Q(forward_task__forward_author__status__icontains=search) |
                Q(forward_task__task__task_title__icontains=search) |
                Q(forward_task__task__task_category__category_title__icontains=search) |
                Q(forward_task__task__task_status__icontains=search) |
                Q(forward_task__task__task_importance_level__icontains=search)
                # Q(forward_task__whom__first_name__icontains= search) |
                # Q(forward_task__whom__last_name__icontains= search)
            )

            assigned_tasks_pinned = assigned_tasks_pinned.filter(
                Q(forward_task__task__task_author__first_name__icontains=search) |
                Q(forward_task__task__task_author__last_name__icontains=search) |
                Q(forward_task__task__task_author__email__icontains=search) |
                Q(forward_task__task__task_author__department__title__icontains=search) |
                Q(forward_task__task__task_author__status__icontains=search) |
                Q(forward_task__task__task_author__status__icontains=search) |
                Q(forward_task__forward_author__first_name__icontains=search) |
                Q(forward_task__forward_author__last_name__icontains=search) |
                Q(forward_task__forward_author__email__icontains=search) |
                Q(forward_task__forward_author__department__title__icontains=search) |
                Q(forward_task__forward_author__status__icontains=search) |
                Q(forward_task__forward_author__status__icontains=search) |
                Q(forward_task__task__task_title__icontains=search) |
                Q(forward_task__task__task_category__category_title__icontains=search) |
                Q(forward_task__task__task_status__icontains=search) |
                Q(forward_task__task__task_importance_level__icontains=search)
                # Q(forward_task__whom__first_name__icontains= search) |
                # Q(forward_task__whom__last_name__icontains= search)
            )

        # Pagination cc_tasks
        page = self.request.GET.get('page')
        paginator = Paginator(assigned_tasks, self.paginate_by)

        try:
            assigned_tasks = paginator.page(page)
        except PageNotAnInteger:
            assigned_tasks = paginator.page(1)
        except EmptyPage:
            assigned_tasks = paginator.page(paginator.num_pages)

        context["assigned_tasks"] = assigned_tasks
        context["assigned_tasks_pinned"] = assigned_tasks_pinned

        return context


class ForwardFormView(LoginRequiredMixin, CreateView):
    model = ForwardTask
    form_class = ForwardForm
    template_name = 'forward/forward_form.html'
    success_url = reverse_lazy('forwarded')

    def get_form_kwargs(self):
        kwargs = super(ForwardFormView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        task_pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=task_pk)
        # Set the task_author to the current user before saving
        form.instance.forward_author = self.request.user
        form.instance.task = task

        try:
            member_statistic = MemberTaskStatistic.objects.get(member=self.request.user, status=True)
        except MemberTaskStatistic.DoesNotExist:
            member_statistic = None

        if member_statistic:
            if member_statistic.created_at.date() != datetime.now().date():
                member_statistic.status = False
                MemberTaskStatistic.objects.create(
                    member=self.request.user,
                    forwarded_task_count=1,
                    assigned_task_count=form.cleaned_data['whom'].count(),
                )
            else:
                member_statistic.forwarded_task_count += 1
                member_statistic.assigned_task_count += form.cleaned_data['whom'].count()

            member_statistic.save()
        else:
            MemberTaskStatistic.objects.create(
                    member=self.request.user,
                    forwarded_task_count=1,
                    assigned_task_count=form.cleaned_data['whom'].count(),
                )

        messages.success(self.request, 'Forward Task successfully sent.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Additional logic can be added here if needed
        messages.error(self.request, 'Could not send the forward task')
        return super().form_invalid(form)


# PIN & DELETE & UNDELETE & DELETE FOREVER

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


def toggle_action_status_forward(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        assigned_id = request.POST.get('assigned_id')
        action_type = request.POST.get('action_type')

        # Check if the task_to_member_action and task_cc_member_action exist
        delete_forwarded_task = ForwardTask.objects.filter(id=task_id, forward_author=request.user).first()
        delete_assigned_task = ForwardedToWhom.objects.filter(id=assigned_id, whom=request.user).first()

        if action_type == 'forward_pin':
            if delete_assigned_task:
                delete_assigned_task.whom_is_pin = not delete_assigned_task.whom_is_pin
                delete_assigned_task.save()

            return JsonResponse({'is_pinned': delete_assigned_task.whom_is_pin if delete_assigned_task else False})

        elif action_type == 'forward_undelete':

            if delete_forwarded_task:
                delete_forwarded_task.forward_author_task_is_deleted = False
                delete_forwarded_task.save()

            if delete_assigned_task:
                delete_assigned_task.whom_is_deleted = False
                delete_assigned_task.save()

            return JsonResponse({'is_deleted':True})

        elif action_type == 'forwarded_task_delete':
            if delete_forwarded_task:
                delete_forwarded_task.forward_author_task_is_deleted = True
                delete_forwarded_task.save()

            if delete_assigned_task:
                delete_assigned_task.whom_is_deleted = True
                delete_assigned_task.save()
            return JsonResponse({'is_deleted': True})

        elif action_type == 'delete_forever_forward':

            if delete_forwarded_task:
                delete_forwarded_task.bin_deleted = True
                delete_forwarded_task.save()

            if delete_assigned_task:
                delete_assigned_task.bin_deleted = True
                delete_assigned_task.save()

            return JsonResponse({'deleted': True})
