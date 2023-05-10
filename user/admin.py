from typing import Any
from django.contrib import admin
from home.admin import admin_site
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, AccessLog

class CustomUserAdmin(UserAdmin):
    """
    Custom user admin page
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    admin_fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name','last_name','phone', 'company_name', 'description')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Address', {'fields':('street_address_1','street_address_2','city','postal_code','country','country_area', 'latitude','longitude')}),
        
    )
    non_admin_fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name','last_name','phone', 'company_name', 'description')}),
        ('Address', {'fields':('street_address_1','street_address_2','city','postal_code','country','country_area', 'latitude','longitude')}),
        
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    def get_queryset(self, request):
        """
        Allows super user to see all users but non superusers can only see themselves.
        """
        if not request.user.is_superuser:
            return User.objects.filter(pk=request.user.pk)
        return super().get_queryset(request)

    def get_fieldsets(self, request, obj=None):
        """
        Allows super users to changes the permissions and important dates but restricts them for non superusers.
        """
        if not request.user.is_superuser:
            return self.non_admin_fieldsets
        return self.admin_fieldsets

class CustomeAccessLog(admin.ModelAdmin):
    """
    Custom access log admin page
    """
    
    model = AccessLog
    list_display = ('email', 'time', 'access_type')
    list_filter = ('email', 'time', 'access_type')
    ordering = ('time',)


admin_site.register(User, CustomUserAdmin)
admin_site.register(Group)
admin_site.register(AccessLog, CustomeAccessLog)
