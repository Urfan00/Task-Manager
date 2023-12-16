from django.db import models
from services.mixins import DateMixin
from Account.models import Account
from services.uploader import Uploader
from ckeditor.fields import RichTextField
from django.contrib.auth.mixins import LoginRequiredMixin



class Task(LoginRequiredMixin, DateMixin):
    status_title = (
        ('Working', 'Working'),
        ('Canceled', 'Canceled'),
        ('Done', 'Done')
    )
    task_title = models.CharField(max_length=255)
    task_image = models.ImageField(upload_to=Uploader.task_image, max_length=255, null=True, blank=True)
    task_content = RichTextField()
    to_members = models.ManyToManyField(Account, related_name='task_to_members')
    cc_members = models.ManyToManyField(Account, related_name='task_cc_members', blank=True)
    task_author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='task_author')
    task_status = models.CharField(max_length=20, choices=status_title)
    task_deadline = models.DateTimeField()
    task_is_flag = models.BooleanField(default=False)
    task_is_read = models.BooleanField(default=False)
    task_is_pin = models.BooleanField(default=False)
    task_is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Task'

