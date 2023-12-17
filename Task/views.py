from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Case, When, Value, BooleanField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class InboxListView(ListView):
    model = Task
    template_name = 'inbox.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        to_task_search = self.request.GET.get('to_task_search', '')
        cc_task_search = self.request.GET.get('cc_task_search', '')

        to_tasks = Task.objects.filter(
                task_to_member_action__to_member=self.request.user
            ).exclude(task_author=self.request.user).distinct().annotate(
            is_view=Case(
                When(task_to_member_action__to_member=self.request.user, task_to_member_action__task_member_is_read=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )

        cc_tasks = Task.objects.filter(
            task_cc_member_action__cc_member=self.request.user
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
                 | Q(task_status__icontains=to_task_search)
                 | Q(task_author__first_name__icontains=to_task_search)
                 | Q(task_author__last_name__icontains=to_task_search)
                 | Q(task_author__department__title__icontains=to_task_search)
                 | Q(task_author__email__icontains=to_task_search)
                 | Q(task_author__status__icontains=to_task_search)
                 | Q(task_author__task_importance_level__icontains=to_task_search)
                 )
        elif cc_task_search:
            cc_tasks = cc_tasks.filter(
                   Q(task_title__icontains=cc_task_search)
                 | Q(task_status__icontains=cc_task_search)
                 | Q(task_author__first_name__icontains=cc_task_search)
                 | Q(task_author__last_name__icontains=cc_task_search)
                 | Q(task_author__department__title__icontains=cc_task_search)
                 | Q(task_author__email__icontains=cc_task_search)
                 | Q(task_author__status__icontains=cc_task_search)
                 | Q(task_author__task_importance_level__icontains=cc_task_search)
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

        return context


class SendTaskListView(ListView):
    model = Task
    template_name = 'send_task.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(task_author=self.request.user).all()

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
        return super().form_valid(form)

    def form_invalid(self, form):
        # Additional logic can be added here if needed
        return super().form_invalid(form)

