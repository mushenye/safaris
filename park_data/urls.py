from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="home"),
    path('services', views.our_services, name="our-services"),

    path('animal/<int:pk>/', views.animal_detail, name='animal'),
    path('about/', views.about, name="about"),
    path('more_about/', views.more_about, name="more_about"),

    path('itineraries/', views.itineraries, name="itineraries"),

    path('contact/', views.contact, name="contact"),
    path('estimate-tour/', views.tour_cost_estimator, name='estimate_tour'),
    path('customer_add/', views.customer_create, name="customer_add"),
    path('compliment/', views.compliment_view, name='compliment'),

    # path('booking/edit/<int:pk>/', views.BookingUpdateView.as_view(), name='booking_edit'),

    path('park/<int:park_id>/vans/', views.touring_vans_list, name='touring_vans_list'),
    path('park/vans/', views.touring_van_all, name='touring_vans_all'),

    path('park/list/', views.park_list_view, name="park_list"),

    path('park/<int:park_id>/accommodations/', views.accommodation_list, name='accommodation_list'),
    path('park/accommodations/', views.accommodation_list_all, name='accommodation_list_all'),
    path('park/accommodations/<int:pk>', views.accommodation_details, name='accommodation_details'),


    # path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('park_create/', views.Park_create.as_view(), name="create_park"),
    path('park/<slug:slug>/', views.ParkDetailView.as_view(), name='park_detail'),


    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('payment/process/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('payment/touring_van/<int:pk>', views.add_touring_van, name='add_touring_van'),
    path('payment/accomodation/', views.add_accommodation, name='add_accommodation'),
    path('payment/add_park/<slug:slug>/', views.add_park, name='add_park'),
    path('payment/view_cart/', views.view_cart, name='view_cart'),
    path('payment/process/', views.process_payment, name='process_payment'),

    path('payment/success/', views.payment_success, name='payment_success'),






]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header= "African Stem Safaris"
admin.site.site_title= "Africa Stem Safaris"
admin.site.site_index_title = "welcome to Africa Stem Safaris"