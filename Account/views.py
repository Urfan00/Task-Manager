from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import ChangePasswordForm, CustomSetPasswordForm, LoginForm, RegistrationForm, ResetPasswordForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import logout



class LogInView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, 'first_time_login') and self.request.user.first_time_login:
                # If user is authenticated and has first_time_login attribute set
                return reverse_lazy('change_password')
            elif next_url:
                # If there's a next_url parameter in the URL, redirect to that
                return next_url
            else:
                return reverse_lazy('index')
        return reverse_lazy('index')  # For anonymous users


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name='change_password.html'
    form_class= ChangePasswordForm
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        # Call the parent class's form_valid method to perform the password change

        # Update the first_time_login attribute to False
        self.request.user.first_time_login = False
        self.request.user.save()

        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return redirect('login')


class ResetPasswordView(PasswordResetView):
    template_name = 'forget-password.html'
    form_class = ResetPasswordForm
    email_template_name = 'reset_password_email.html'
    subject_template_name = 'reset_password_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      "If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."

    success_url = reverse_lazy('logout')


class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name='reset_password_confirm.html'
    form_class=CustomSetPasswordForm
    success_url = reverse_lazy('logout')
