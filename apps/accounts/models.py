from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser, TimeStampedModel):
    """
    Custom User model that extends Django's AbstractUser and includes
    timestamp fields for created and modified times.
    """
    EMPLOYEE_ADMIN = 'employee-admin'
    GYM_MEMBER = 'gym-member'

    ROLE_CHOICES = [
        (EMPLOYEE_ADMIN, 'Employee Admin'),
        (GYM_MEMBER, 'Gym Member'),
    ]

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=GYM_MEMBER)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.role})"

    def save(self, *args, **kwargs):
        # Set a default password if none is provided
        if not self.pk and not self.password:  # Only for new users
            self.set_password('defaultpassword123')

        # Ensure gym members must change their password on first login
        if self.role == self.GYM_MEMBER:
            self.must_change_password = True

        super().save(*args, **kwargs)