from django.db import models
from django.extensions import TimestampedModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, TimestampedModel):
    """
    Custom User model that extends Django's AbstractUser and includes
    timestamp fields for created and modified times.
    """
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'