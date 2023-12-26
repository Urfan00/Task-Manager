from django.db import models
from services.mixins import DateMixin
from Account.models import Account
from services.uploader import Uploader
from ckeditor.fields import RichTextField




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


class Task(DateMixin):
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


class TaskActionLog(DateMixin):
    log_author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='log_author')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='log_task')
    old_status = models.CharField(max_length=20, choices=Task.status_title, null=True, blank=True)
    new_status = models.CharField(max_length=20, choices=Task.status_title, null=True, blank=True)

    def __str__(self):
        return f"{self.log_author.first_name} {self.log_author.last_name} - {self.task.task_title}"

    class Meta:
        verbose_name = 'Task Action Log'
        verbose_name_plural = 'Task Action Log'


class ForwardTask(DateMixin):
    forward_author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author_forward')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_forward')
    forward_author_content = RichTextField(null=True, blank=True)
    forward_author_task_is_deleted = models.BooleanField(default=False)
    bin_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.forward_author.get_full_name()} - {self.task.task_title}"

    class Meta:
        verbose_name = 'Forward Task'
        verbose_name_plural = 'Forward Task'


class ForwardedToWhom(DateMixin):
    whom = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='whom')
    forward_task = models.ForeignKey(ForwardTask, on_delete=models.CASCADE, related_name='forward_task')
    whom_is_read = models.BooleanField(default=False)
    whom_is_pin = models.BooleanField(default=False)
    whom_is_deleted = models.BooleanField(default=False)
    bin_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.whom.get_full_name()

    class Meta:
        verbose_name = 'Forwarded To Whom'
        verbose_name_plural = 'Forwarded To Whom'
