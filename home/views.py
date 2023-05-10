from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from user.forms import ProfileChangeForm

from django.contrib.auth import logout
from django.shortcuts import redirect
import folium
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

User = get_user_model()

def index_view(request):
   """
   homepage index view that redirects to the login page if the user is not authenticated
   """
   if request.user.is_authenticated:
      return redirect('/map/')
   else:
      return redirect('/accounts/login/')
   
def logout_view(request):
  """
  dashboard logout redirect view
  """
  logout(request)
  return redirect('/accounts/login/')

class UserLoginView(LoginView):
  """
  for users of the dashboard to login
  """
  template_name = 'accounts/login.html'
  form_class = LoginForm

class ProtectedProfileView(TemplateView):
  """
  this view is for users that are logged in to access their profile
  """
  template_name = "pages/profile.html"

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)
  
  def get_context_data(self, **kwargs):
    """
    This injects the map object into the context
    """
    context = super().get_context_data(**kwargs)
    usr_obj = self.request.user
    context['segment'] = 'profile'
    context['user'] = usr_obj

    if usr_obj.latitude != None:
      map = folium.Map(location=[usr_obj.latitude, usr_obj.longitude], zoom_start=4)
      folium.Marker([usr_obj.latitude, usr_obj.longitude]).add_to(map)
    else:
      map = folium.Map()
    map_html = map._repr_html_()
    context['map'] = map_html

    return context
  
class ProtectedProfileEditView(UpdateView):
  """
  This protected view is to update the user profile
  """
  template_name = "pages/profile-edit.html"
  form_class = ProfileChangeForm
  success_url = "/profile/"
  model = User

  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)

  def get_object(self):
    return self.request.user

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['segment'] = 'profile'
    return context


class ProtectedMapView(TemplateView):
    template_name = "pages/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        This gets all users that have a valid coordinates and add them to the map object, and inject into the context
        """
        context = super().get_context_data(**kwargs)
        map = folium.Map(location=[19,-12], zoom_start=2)

        usr_objs = User.objects.all()

        for usr_obj in usr_objs:
          address = ', '.join(filter(None, 
                      (usr_obj.street_address_1,
                      usr_obj.street_address_2,  
                      usr_obj.city,
                      usr_obj.country.name,
                      usr_obj.postal_code)
                      ))
          popup = render_to_string('layouts/popup.html', { 'user': usr_obj, 'address': address })

          if usr_obj.latitude is not None:
            folium.Marker([usr_obj.latitude, usr_obj.longitude], tooltip="click here for more info", popup=popup).add_to(map)

        map_html = map._repr_html_()
        context['map'] = map_html
        context['segment'] = 'map'

        return context
       
    



