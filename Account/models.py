from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from services.uploader import Uploader
from services.mixins import DateMixin
from ckeditor.fields import RichTextField



class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, FIN=None, number=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        user = self.model(email=self.normalize_email(email), FIN=FIN, number=number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, FIN=None, number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if email is None:
            raise ValueError('The Email field must be set for superusers.')

        return self.create_user(email, FIN, number, password, **extra_fields)



class Department(DateMixin):
    title = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Department'


class Account(AbstractUser):
    FIN = models.CharField(max_length=21, unique=True)
    email = models.EmailField(unique=True, max_length=254)
    number = models.CharField(max_length=20)
    image = models.ImageField(upload_to=Uploader.user_image, null=True, blank=True, max_length=255)
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    department = models.OneToOneField(Department, on_delete=models.CASCADE, related_name='user_department', null=True, blank=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['FIN', 'number']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Set the password to FIN if it's not already set
        if not self.password:
            self.set_password(self.FIN)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'


class UserStatus(DateMixin):
    first_time_login = models.BooleanField(default=True)
    head_of_department = models.BooleanField(default=False)
    assistant = models.BooleanField(default=True)
    staff_department = models.BooleanField(default=True)
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='user_status')

    def __str__(self):
        return f"{self.account.first_name} {self.account.last_name}"

    class Meta:
        verbose_name = 'User Status'
        verbose_name_plural = 'User Status'
