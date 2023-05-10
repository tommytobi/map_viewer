from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    User model that modifies the base user and add Permissions mixin for groups
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    company_name = models.CharField(_('company name'), max_length=30, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone = PhoneNumberField(blank=True, default="")

    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField(null=True, blank=True)
    country_area = models.CharField(max_length=128, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


LOGIN_CHOICES = (
    ("LOGIN", "Login"),
    ("LOGOUT", "Logout"),
    ("ATTEMPT", "Attempt")
)

class AccessLog(models.Model):
    """
    access log model to keep track of when a user logs in or out or attempts to login
    """
    email = models.CharField(_('email address'), max_length=30)
    time = models.DateTimeField(_('time accessed'),default=timezone.now)
    access_type = models.CharField(max_length=10,
                                   choices=LOGIN_CHOICES,
                                   default="LOGIN")
    
    def __str__(self):
        return self.email