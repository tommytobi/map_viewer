from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AuthenticationForm


class CustomAdminSite(AdminSite):
    login_form = AuthenticationForm
    site_header = 'Map Viewer Admin'

    def has_permission(self, request):
        """
        Checks if the current user has access.
        """
        return request.user.is_active

admin_site = CustomAdminSite(name="myadmin")
