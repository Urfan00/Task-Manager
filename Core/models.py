from django.db import models
from Account.models import Account
from services.mixins import DateMixin



class MemberTaskStatistic(DateMixin):
    member = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='send_statistic_author')
    sent_task_count = models.PositiveIntegerField(default=0)
    to_task_count = models.PositiveIntegerField(default=0)
    cc_task_count = models.PositiveIntegerField(default=0)
    forwarded_task_count = models.PositiveIntegerField(default=0)
    assigned_task_count = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.member.get_full_name()

    class Meta:
        verbose_name = 'Member Task Statistic'
        verbose_name_plural = 'Member Task Statistic'
