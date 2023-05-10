from django.urls import include, path
from home.admin import admin_site

urlpatterns = [
    path('', include('home.urls')),
    path("admin/", admin_site.urls),
    path("", include('admin_soft.urls'))
]
