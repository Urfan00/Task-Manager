from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Task
from .forms import TaskForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin



def inbox(request):
    return render(request, 'inbox.html')

def send_task(request):
    return render(request, 'inbox.html')



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

