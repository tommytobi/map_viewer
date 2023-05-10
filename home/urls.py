from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('map/', views.ProtectedMapView.as_view(), name='map'),
    path('profile/', views.ProtectedProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProtectedProfileEditView.as_view(), name='profile-edit'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
