from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class User(AbstractUser):

    username = None

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('GENERAL_USER', 'General User'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES, default='GENERAL_USER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name']

    objects = UserManager()

    def __str__(self):
        return self.email