
from django.contrib import admin
from django.urls import include,path


handler404 = 'park_data.views.custom_404'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('park_data.urls')),
    path('', include('user.urls')),
    
]

