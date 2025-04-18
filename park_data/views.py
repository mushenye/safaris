from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from park_data.forms import BookingForm, CustomerForm, ParkCreateForm,TourCostEstimatorForm
from park_data.models import Animal, BookPark, Customer, Park, ParkList, Accommodation
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages

def index(request):
    return render(request, 'park_data/home.html')

def about(request):
    return render(request, 'park_data/about.html')

def itineraries(request):
    return render(request, 'park_data/itineraries.html')

def custom_404(request, exception):
    return render(request, 'parK_data/not_found.html', status=404)


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


# class CustomerCreateView(CreateView):
#     model = Customer
#     form_class = CustomerForm
#     template_name = 'park_data/customer_form.html'

#     def get_success_url(self):
#         return reverse('booking_add', kwargs={'customer_id': self.object.id})
    
#     def get_queryset(self):
#         return super().get_queryset()
    
  
def customer_create(request, slug):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            instance = form.save()

            park = get_object_or_404(Park, slug=slug)

            # Create booking with the customer instance
            new_booking = BookPark.objects.create(
                park=park,
                customer=instance
            )

            return redirect('booking_edit', new_booking.id)

    return render(request, 'park_data/customer_form.html', {'form': form})






class BookingUpdateView(UpdateView):
    model = BookPark
    form_class = BookingForm
    template_name = 'park_data/booking_form.html'
    success_url = reverse_lazy('park_list')  

    def form_valid(self, form):
        response = super().form_valid(form)

        customer = self.object.customer
        park = self.object.park
        due_date = self.object.due_date
        created=self.object.created
        
        message = (
            f"Hello {customer.first_name},\n\n"
            f"Your booking scheduled for {due_date} to tour {park.name} has been recieved on {created}.\n Our customer service team will call you \n\n"
            f"Thank you!\n\nRegards,\nAfrica Stem Safaris"
        )
        subject= f"RE: {customer.first_name}- Booking recieved"

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[customer.email],
                fail_silently=False,
            )
            messages.success(self.request, "Booking updated and email sent successfully!")
        except Exception as e:
            messages.warning(self.request, f"Booking updated but email failed to send: {e}")

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_park'] = self.object
        return context





def park_list_view(request):
    country = request.GET.get('country')
    query=request.GET.get('q')

    parks = Park.objects.all()
    if country or query:
        parks = (parks.filter(country__iexact=country) or parks.filter(slug__icontains=query))
    
    paginator = Paginator(parks, 8)  # 8 parks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'parks': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    return render(request, 'park_data/parks.html', context)






def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Message from {name.capitalize()} <{email.lower()}>:\n\n{message}"
            
            try:
                send_mail(
                    subject,
                    full_message,
                    email,
                    ['mpsimani01@gmail.com'], 
                    fail_silently=False,
                )
                messages.success(request, 'Message sent successfully!')
                return redirect('contact')
            except:
                messages.warning(request, 'Error in sending Please try again!')
                return redirect('contact')
            

    return render(request, 'park_data/contact.html', {'form': form})




def tour_cost_estimator(request):
    total_cost = None
    if request.method == 'POST':
        form = TourCostEstimatorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            num_people = data['number_of_people']
            num_days = data['number_of_days']

            # Base cost per person
            accommodation = data['accommodation_per_night'] * num_days
            meals = data['meals_per_day'] * num_days
            park_fees = data['park_entry_fee']
            
            # Total cost before profit
            base_total = (
                data['transport_cost'] +
                (accommodation + meals + park_fees) * num_people +
                data['guide_fee'] +
                data['misc']
            )

            # Add profit
            margin = data['profit_margin']
            total_cost = base_total + (base_total * margin / 100)

    else:
        form = TourCostEstimatorForm()

    return render(request, 'park_data/tour_cost_estimator.html', {'form': form, 'total_cost': total_cost})


def accommodation_list(request, park_id):
    park = get_object_or_404(Park, id=park_id)
    accommodations = park.accommodations.all()
    return render(request, 'park_data/acom_list.html', {'accommodations': accommodations, 'park': park})


def touring_vans_list(request, park_id):
    park = get_object_or_404(Park, id=park_id)
    vans = park.vans.all()
    return render(request, 'park_data/touring_vans_list.html', {'vans': vans, 'park': park})



def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)

    habitat=[ (animal.habitat_image1, 'Hunting Grounds'),
             (animal.habitat_image2, 'Watering Spot'), 
             (animal.habitat_image3, 'RestingArea') 
             ]
    
    context = {
        'animal': animal,
        'habitat':habitat
    }
    return render(request, 'park_data/animal.html', context)