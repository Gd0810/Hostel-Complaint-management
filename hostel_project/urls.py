from django.contrib import admin as django_admin
from django.urls import path, include

urlpatterns = [
    path('admin/', django_admin.site.urls),
    path('', include('complaints.urls')),
]