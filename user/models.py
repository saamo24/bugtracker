from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('teamlead', 'Team Lead'),
        ('developer', 'Developer'),
        ('tester', 'Tester'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='developer')

    objects = UserManager()

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
