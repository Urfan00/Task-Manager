from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Account
from .resources import AccountResource
from .forms import ChangePasswordForm, CustomSetPasswordForm, ExcelForm, LoginForm, RegistrationForm, ResetPasswordForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages
from django.views import View
from tablib import Dataset
from django.http import HttpResponse
from openpyxl import Workbook
from django.db import IntegrityError



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


class RegisterView(View):
    model = Account
    template_name = 'register.html'

    def get_context_data(self):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        excelform = ExcelForm()
        return render(request, self.template_name, {**self.get_context_data(), 'form': form, 'excelform': excelform})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST, request.FILES)
        excelform = ExcelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(self.request, 'Successfully registered.')
            return redirect('register')
        elif excelform.is_valid():
            account_resource = AccountResource()
            dataset = Dataset()
            new_users = request.FILES['excel_file']

            if not new_users.name.endswith('xlsx'):
                messages.info(self.request, 'Format should be .xlsx')
                return redirect('register')

            imported_data = dataset.load(new_users.read(), format='xlsx')

            failed_users = []

            for data in imported_data:
                data = list(data)

                try:
                    Account.objects.create(
                        first_name=data[0],
                        last_name=data[1],
                        number=data[2],
                        email=data[3],
                        FIN=data[4],
                        department=data[5],
                        status=data[6],
                    )
                except IntegrityError as e:
                    if 'UNIQUE constraint failed: Account_account.email' in str(e):
                        # Handle the case where the email already exists
                        failed_users.append(data)

            if failed_users:
                # Create a new Excel file with failed users
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="failed_users.xlsx"'

                workbook = Workbook()
                worksheet = workbook.active

                # Add headers
                headers = ['First Name', 'Last Name', 'Number', 'Email', 'FIN', 'Department', 'Status']
                worksheet.append(headers)

                # Add failed users
                for failed_user in failed_users:
                    worksheet.append(failed_user)

                workbook.save(response)
                messages.warning(self.request, 'Some users dont imported.')
                return redirect('register')
                # return response
            else:
                messages.success(self.request, 'Successfully imported all users.')
                return redirect('register')
        else:
            messages.error(request, 'Don\'t registered')
            return redirect('register')


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name='change_password.html'
    form_class= ChangePasswordForm
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        # Call the parent class's form_valid method to perform the password change

        # Update the first_time_login attribute to False
        self.request.user.first_time_login = False
        self.request.user.save()

        messages.success(self.request, 'Password changed successfully.')
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
