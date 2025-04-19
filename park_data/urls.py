from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="home"),
    path('animal/<int:pk>/', views.animal_detail, name='animal'),
    path('about/', views.about, name="about"),
    path('itineraries/', views.itineraries, name="itineraries"),

    path('contact/', views.contact, name="contact"),
    path('estimate-tour/', views.tour_cost_estimator, name='estimate_tour'),
    path('customer_add/', views.customer_create, name="customer_add"),

    # path('booking/edit/<int:pk>/', views.BookingUpdateView.as_view(), name='booking_edit'),

    path('park/<int:park_id>/vans/', views.touring_vans_list, name='touring_vans_list'),

    path('park/list/', views.park_list_view, name="park_list"),
    path('park/<int:park_id>/accommodations/', views.accommodation_list, name='accommodation_list'),

    # path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('park_create/', views.Park_create.as_view(), name="create_park"),
    path('park/<slug:slug>/', views.ParkDetailView.as_view(), name='park_detail'),


    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment/process/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('payment/touring_van/', views.add_touring_van, name='add_touring_van'),
    path('payment/accomodation/', views.add_accommodation, name='add_accommodation'),
    path('payment/add_park/<slug:slug>/', views.add_park, name='add_park'),
    path('payment/view_cart/', views.view_cart, name='view_cart'),






]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header= "Afican Stem Safaris"
admin.site.site_title= "Africa Stem Safaris"
admin.site.site_index_title = "welcome to Africa Stem Safaris"