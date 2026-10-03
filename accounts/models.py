<<<<<<< HEAD
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
=======
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
>>>>>>> 7159795b6044deffa8701f4b9b7a29f57ca8987b
        return self.email