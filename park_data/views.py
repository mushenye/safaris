from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from django.core.paginator import Paginator
from park_data.forms import BookingForm, CustomerForm, ParkCreateForm
from park_data.models import Booking, Customer, Park

def index(request):
    return render(request, 'park_data/home.html')
def about(request):
    return render(request, 'park_data/about.html')


class Park_create(CreateView):
    model = Park
    form_class = ParkCreateForm
    template_name = 'park_data/park_form.html'
    success_url = reverse_lazy('park_list')  # Redirect after success


class ParkDetailView(DetailView):
    model = Park
    template_name = 'park_data/park_detail.html'
    context_object_name = 'park'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'park_data/customer_form.html'

    def get_success_url(self):
        # self.object is the saved Customer instance
        return reverse('booking_add', kwargs={'customer_id': self.object.id})


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'park_data/booking_form.html'
    success_url = reverse_lazy('/')  

    def form_valid(self, form):
        customer_id = self.kwargs.get('customer_id')
        form.instance.customer = get_object_or_404(Customer, pk=customer_id)
        return super().form_valid(form)


def park_list_view(request):
    country = request.GET.get('country')
    parks = Park.objects.all()
    if country:
        parks = parks.filter(country__iexact=country)
    
    paginator = Paginator(parks, 8)  # 8 parks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'parks': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'park_data/parks.html', context)