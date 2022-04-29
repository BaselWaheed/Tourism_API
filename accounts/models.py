from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given email must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self,username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('staff must have is_staff=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    type = [
        ("male","male"),
        ("female","female"),
    ]
    username = models.CharField(_('username'), max_length=50, blank=True,unique=True, null = True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null = True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null = True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    country = models.CharField(blank=True , max_length=30, null = True)
    date_of_birth = models.DateField(null = True)
    gender = models.CharField( max_length=50,choices=type, null = True)
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    def __str__(self):
        return self.username

class PhoneNumber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(unique=True, blank=True , max_length=11, null = True)
    is_verified = models.BooleanField(default=False)

  

    def __str__(self):
        return self.phone


class EmailAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, blank=False)
    is_verified = models.BooleanField(default=False)
  

    def __str__(self):
        return self.email


