from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import LoginForm, RegistrationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin


class LogInView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    # def get(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         return redirect('admin')
    #     return super().get(request, *args, **kwargs)

    # def get_success_url(self):
    #     next_url = self.request.GET.get('next', None)
        
    #     if self.request.user.is_authenticated:
    #         if hasattr(self.request.user, 'first_time_login') and self.request.user.first_time_login:
    #             # If user is authenticated and has first_time_login attribute set
    #             return reverse_lazy('change_password')
    #         elif next_url:
    #             # If there's a next_url parameter in the URL, redirect to that
    #             return next_url
    #         else:
    #             return reverse_lazy('index')
    #     return reverse_lazy('index')  # For anonymous users


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')