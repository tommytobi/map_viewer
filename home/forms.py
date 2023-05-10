
from django import forms

from django.contrib.auth.forms import AuthenticationForm,  UsernameField
from django.utils.translation import gettext_lazy as _


class LoginForm(AuthenticationForm):
  """
  User login form for the dashboard
  """
  username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}))
  password = forms.CharField(
      label=_("Password"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
  )