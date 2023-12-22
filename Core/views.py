from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from Account.models import Account
from .forms import AccountEditForm
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages



def index(request):
    return render(request, 'dashboard.html')


class ProfileView(LoginRequiredMixin, View):
    model = Account
    template_name = 'profile.html'

    def get_context_data(self):
        context = {}
        context["account_user"] = Account.objects.filter(id=self.request.user.pk).first()
        return context

    def get(self, request, *args, **kwargs):
        form = AccountEditForm(instance=request.user)
        return render(request, self.template_name, {**self.get_context_data(), 'form': form})

    def post(self, request, *args, **kwargs):
        form = AccountEditForm(request.POST, request.FILES)

        if form.is_valid():
            user_account = Account.objects.get(pk=request.user.pk)
            user_account.number = form.cleaned_data.get('number')
            user_account.bio = form.cleaned_data.get('bio')
            # user_account.image = form.cleaned_data.get('image')
            if form.cleaned_data.get('image'):
                user_account.image = form.cleaned_data.get('image')
            elif 'image' in form.cleaned_data and not form.cleaned_data['image'] is None:
                user_account.image = None
            user_account.save()
            messages.success(request, 'Profile changed successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Məlumatlarınız yenilənmədi')
            return redirect('profile')
