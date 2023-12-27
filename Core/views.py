from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from Account.models import Account
from .models import MemberTaskStatistic
from .forms import AccountEditForm
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone



class InboxView(LoginRequiredMixin, ListView):
    model = MemberTaskStatistic
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        today_statistic = MemberTaskStatistic.objects.filter(member=self.request.user, created_at__date=today).first()
        yesterday_statistic = MemberTaskStatistic.objects.filter(member=self.request.user, created_at__date=yesterday).first()

        if today_statistic:
            if yesterday_statistic and yesterday_statistic.sent_task_count != 0:
                percent_change = ((today_statistic.sent_task_count - yesterday_statistic.sent_task_count) / yesterday_statistic.sent_task_count) * 100
            else:
                percent_change = 100
            context["percent_sent_task"] = percent_change

            if yesterday_statistic and yesterday_statistic.forwarded_task_count != 0:
                percent_change = ((today_statistic.forwarded_task_count - yesterday_statistic.forwarded_task_count) / yesterday_statistic.forwarded_task_count) * 100
            else:
                percent_change = 100
            context["percent_forwarded_task"] = percent_change

            if yesterday_statistic and yesterday_statistic.assigned_task_count != 0:
                percent_change = ((today_statistic.assigned_task_count - yesterday_statistic.assigned_task_count) / yesterday_statistic.assigned_task_count) * 100
            else:
                percent_change = 100
            context["percent_assigned_task"] = percent_change

            if yesterday_statistic and yesterday_statistic.to_task_count != 0:
                percent_change = ((today_statistic.to_task_count - yesterday_statistic.to_task_count) / yesterday_statistic.to_task_count) * 100
            else:
                percent_change = 100
            context["percent_to_task"] = percent_change

            if yesterday_statistic and yesterday_statistic.cc_task_count != 0:
                percent_change = ((today_statistic.cc_task_count - yesterday_statistic.cc_task_count) / yesterday_statistic.cc_task_count) * 100
            else:
                percent_change = 100
            context["percent_cc_task"] = percent_change

            context["todays_task"] = today_statistic

        # Weekly statistic
        this_week_start = today - timedelta(days=today.weekday())
        this_week_end = this_week_start + timedelta(days=6)

        last_week_start = this_week_start - timedelta(days=7)
        last_week_end = last_week_start + timedelta(days=6)

        last_week_statistic = MemberTaskStatistic.objects.filter(member=self.request.user, created_at__date__range=[last_week_start, last_week_end])
        this_week_statistic = MemberTaskStatistic.objects.filter(member=self.request.user, created_at__date__range=[this_week_start, this_week_end])

        if this_week_statistic:
            this_week_sent_count = sum([stat.sent_task_count for stat in this_week_statistic])
            context["this_week_sent_count"] = this_week_sent_count
            last_week_sent_count = sum([stat.sent_task_count for stat in last_week_statistic])

            if last_week_sent_count != 0:
                percent_change = ((this_week_sent_count - last_week_sent_count) / last_week_sent_count) * 100
            else:
                percent_change = 100

            context["percent_sent_week"] = percent_change


            this_week_to_count = sum([stat.to_task_count for stat in this_week_statistic])
            context["this_week_to_count"] = this_week_to_count
            last_week_to_count = sum([stat.to_task_count for stat in last_week_statistic])

            if last_week_to_count != 0:
                percent_change = ((this_week_to_count - last_week_to_count) / last_week_to_count) * 100
            else:
                percent_change = 100

            context["percent_to_week"] = percent_change


            this_week_cc_count = sum([stat.cc_task_count for stat in this_week_statistic])
            context["this_week_cc_count"] = this_week_cc_count
            last_week_cc_count = sum([stat.cc_task_count for stat in last_week_statistic])

            if last_week_cc_count != 0:
                percent_change = ((this_week_cc_count - last_week_cc_count) / last_week_cc_count) * 100
            else:
                percent_change = 100

            context["percent_cc_week"] = percent_change

            this_week_forwarded_count = sum([stat.forwarded_task_count for stat in this_week_statistic])
            last_week_forwarded_count = sum([stat.forwarded_task_count for stat in last_week_statistic])

            this_week_assigned_count = sum([stat.assigned_task_count for stat in this_week_statistic])
            last_week_assigned_count = sum([stat.assigned_task_count for stat in last_week_statistic])

            context["this_week_statistic"] = this_week_statistic


        return context


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
