from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import AccessLog
 
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    signal reciever that logs a login
    """
    AccessLog.objects.create(
        email = user.email, 
        access_type= "LOGIN"
        )

 
 
@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    """
    Signal reciever that logs a login attempt
    """
    AccessLog.objects.create(
        email = credentials['username'], 
        access_type= "ATTEMPT"
        )

 
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """
    signal reciever that logs a logout
    """
    AccessLog.objects.create(
        email = user.email, 
        access_type= "LOGOUT"
        )
