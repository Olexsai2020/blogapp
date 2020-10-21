from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('', include('members.urls')),
]