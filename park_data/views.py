from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from park_data.forms import BookingForm, CustomerForm, ParkCreateForm
from park_data.models import BookPark, Customer, Park
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages

def index(request):
    return render(request, 'park_data/home.html')

def about(request):
    return render(request, 'park_data/about.html')

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



# def booking_edit(request, pk):
#     book_park=BookPark.objects.get( id =pk)
#     if request.method== 'POST':
#         form=BookingForm(request.POST,instance=book_park)
#         if form.is_valid():
#             form.save()
#             return redirect('park_list')
#     else:
#         form=BookingForm(instance=book_park)
#     return render(request, 'park_data/booking_form.html', {'form':form, 'book_park':book_park})



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

        # Compose email message
        message = (
            f"Hello {customer.first_name},\n\n"
            f"Your booking scheduled for {due_date} to tour {park.name} has been updated.\n\n"
            f"Thank you!\n\nRegards,\nAfrica Stem Safaris"
        )

        try:
            send_mail(
                subject='Your Booking Has Been Updated',
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
            
            print(full_message)
            try:
                send_mail(
                    subject,
                    full_message,
                    email,
                    ['your_email@gmail.com'], 
                    fail_silently=False,
                )
                messages.success(request, 'Message sent successfully!')
                return redirect('contact')
            except:
                messages.warning(request, 'Error in sending Please try again!')
                return redirect('contact')
            

    return render(request, 'park_data/contact.html', {'form': form})
