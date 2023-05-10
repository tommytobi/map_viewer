from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django import forms
from .models import User
from .utils import get_lat_lng

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = "__all__"




class CustomUserChangeForm(UserChangeForm):
    """
    This user change form is used in the admin view to update the user permissions and important dates
    """
    phone = PhoneNumberField(region="ZA")

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs): 
        """
        This is used to disable fields which no user should update
        """
        super(CustomUserChangeForm, self).__init__(*args, **kwargs) 
        if 'email' in self.fields:                          
            self.fields['email'].disabled = True
        if 'latitude' in self.fields:
            self.fields['latitude'].disabled = True
        if 'longitude' in self.fields:
            self.fields['longitude'].disabled = True

    def clean(self):
        """
        This function tries to get the latlng details and raises a validation error is no latlng geocode is found 
        """
        cleaned_data = super().clean()
        locationTupple = (
            cleaned_data.get("street_address_1", None),
            cleaned_data.get("street_address_2", None),
            cleaned_data.get("city", None),
            cleaned_data.get("country", None),
        )
        location = '+'.join(filter(None, locationTupple))
        lat, lng = get_lat_lng(location)


        if lat == None or lng == None:
            raise ValidationError("Please review your address, could not find geocode.")

        cleaned_data['latitude'] = lat
        cleaned_data['longitude'] = lng
        
        return cleaned_data

        
class ProfileChangeForm(forms.ModelForm):
    """
    This form is used to update a standard users information, which excludes permissions and login information
    """
    class Meta:
        model = User
        exclude = ('email', 'password', 'user_permissions', 'groups', 'is_superuser' ,'is_staff','is_active','is_active', 'last_login', 'date_joined')

    def __init__(self, *args, **kwargs): 
        """
        This is used to disable fields which no user should update
        """
        super().__init__(*args, **kwargs) 
        if 'email' in self.fields:                          
            self.fields['email'].disabled = True
        if 'latitude' in self.fields:
            self.fields['latitude'].disabled = True
        if 'longitude' in self.fields:
            self.fields['longitude'].disabled = True

    def clean(self):
        """
        This function tries to get the latlng details and raises a validation error is no latlng geocode is found 
        """

        cleaned_data = super().clean()
        locationTupple = (
            cleaned_data.get("street_address_1", None),
            cleaned_data.get("street_address_2", None),
            cleaned_data.get("city", None),
            cleaned_data.get("country", None),
        )
        location = '+'.join(filter(None, locationTupple))
        lat, lng = get_lat_lng(location)


        if lat == None or lng == None:
            raise ValidationError("Please review your address, could not find geocode.")

        cleaned_data['latitude'] = lat
        cleaned_data['longitude'] = lng
        
        return cleaned_data
    