from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('park/list/', views.park_list_view, name="park_list"),

    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('park_create/', views.Park_create.as_view(), name="create_park"),
    path('park/<slug:slug>/', views.ParkDetailView.as_view(), name='park_detail'),
    path('bookings/add/<int:customer_id>', views.BookingCreateView.as_view(), name='booking_add'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
