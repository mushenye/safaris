from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from park_data.forms import ParkCreateForm
from park_data.models import Park

def index(request):
    return HttpResponse("<h1>Welcome to our site </h1>")



class Park_create(CreateView):
    model = Park
    form_class = ParkCreateForm
    template_name = 'park_data/park_form.html'
    success_url = reverse_lazy('park_list')  # Redirect after success

