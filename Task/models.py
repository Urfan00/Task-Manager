from django.db import models
from services.mixins import DateMixin
from Account.models import Account
from services.uploader import Uploader
from ckeditor.fields import RichTextField
from django.contrib.auth.mixins import LoginRequiredMixin




class TaskCategory(DateMixin):
    category_title = models.CharField(max_length=255)

    def __str__(self):
        return self.category_title

    class Meta:
        verbose_name = 'Task Category'
        verbose_name_plural = 'Task Category'


class TaskToMembersAction(DateMixin):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='task_to_member_action')
    to_member = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='task_to_members', null=True, blank=True)
    task_member_is_read = models.BooleanField(default=False)
    task_member_is_pin = models.BooleanField(default=False)
    task_member_is_deleted = models.BooleanField(default=False)
    bin_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.task_title} members : {self.to_member}"

    class Meta:
        verbose_name = 'Task to Members Action'
        verbose_name_plural = 'Task to Members Action'


class TaskCCMembersAction(DateMixin):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='task_cc_member_action')
    cc_member = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='task_cc_members', null=True, blank=True)
    task_member_is_read = models.BooleanField(default=False)
    task_member_is_pin = models.BooleanField(default=False)
    task_member_is_deleted = models.BooleanField(default=False)
    bin_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.task_title} members : {self.cc_member}"


    class Meta:
        verbose_name = 'Task cc Members Action'
        verbose_name_plural = 'Task cc Members Action'


class Task(LoginRequiredMixin, DateMixin):
    status_title = (
        ('Working', 'Working'),
        ('Canceled', 'Canceled'),
        ('Done', 'Done')
    )
    importance_level_status = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )
    task_title = models.CharField(max_length=255)
    task_image = models.ImageField(upload_to=Uploader.task_image, max_length=255, null=True, blank=True)
    task_content = RichTextField()
    task_author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='task_author')
    task_status = models.CharField(max_length=20, choices=status_title, null=True, blank=True) # status create olan qoyulsun yoxsa edit olanda
    task_importance_level = models.CharField(max_length=20, choices=importance_level_status)
    task_deadline = models.DateTimeField()
    task_author_is_deleted = models.BooleanField(default=False)
    task_category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name='task_category')
    bin_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.task_title

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Task'
