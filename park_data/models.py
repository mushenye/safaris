from django.db import models
from django.template.defaultfilters import slugify
import uuid

class ParkList(models.Model):
    park_image=models.ImageField(upload_to='park_images/')
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Park(models.Model):
    country = models.CharField( choices= (
        ('Kenya', 'Kenya'),
        ('Uganda','Uganda'),
        ('Tanzania','Tanzania'),
    ),max_length=100)
    name = models.ForeignKey(ParkList, on_delete=models.CASCADE,)
    location = models.CharField(max_length=255, help_text="Nearest city or coordinates")
    established_date = models.DateField(null=True, blank=True)
    size_sq_km = models.FloatField(null=True, blank=True, help_text="Size in square kilometers")
    journey_description = models.TextField( )
    history = models.TextField()
    flora_and_fauna = models.TextField(help_text="Details about wildlife and plants seen at the park")
    climate = models.TextField(blank=True, help_text="Weather and best time to visit")
    booking_info = models.TextField(help_text="How visitors can book or contact you")
    slug=models.SlugField(blank=True, null=True, unique=True)

    def get_slug_string(self):
        elements = [self.name.name.lower(), self.country.lower()]
        filtered_elements = filter(None, elements)
        return ' '.join(filtered_elements)
    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.get_slug_string())
            self.slug = base_slug
            if Park.objects.filter(slug=self.slug).exists():
                self.slug = f'{base_slug}-{uuid.uuid4().hex[:6]}'
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name.name
    
    
class Information(models.Model):
    park = models.ForeignKey(Park, related_name='important_information', on_delete=models.CASCADE)
    important_information = models.TextField(help_text="Rules, regulations, health precautions")
    
    
    def __str__(self):
        return f"Information for {self.park.name}"
    

class Park_Highlight(models.Model):
    park = models.ForeignKey(Park, related_name='highlights', on_delete=models.CASCADE)
    highlights = models.TextField()

    def __str__(self):
        return f"Highlight for {self.park.name}"
    

    

class ParkImage(models.Model):
    park = models.ForeignKey(Park, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='park_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.park.name}"


class HowToGetThere(models.Model):
    park = models.OneToOneField(Park, related_name='travel_info', on_delete=models.CASCADE)
    by_road = models.TextField()
    by_air = models.TextField()
    journey_details = models.TextField()

    def __str__(self):
        return f"How to get to {self.park.name}"


class EntryFee(models.Model):
    park = models.ForeignKey(Park, related_name='entry_fees', on_delete=models.CASCADE)
    visitor_type = models.CharField(max_length=50, choices=[
        ('local', 'Local Visitor'),
        ('foreign', 'Foreign Visitor'),
        ('child', 'Child'),
        ('student', 'Student'),
    ])
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.visitor_type} - {self.amount}"


class Accommodation(models.Model):
    park = models.ForeignKey(Park, related_name='accommodations', on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    contact_info = models.TextField()

    def __str__(self):
        return f"{self.name} in {self.park.name}"



    

class Customer (models.Model):
    created=models.DateField(auto_now_add=True)
    first_name= models.CharField(max_length=100)
    middle_name= models.CharField(max_length=100, blank=True, null=True)    
    last_name= models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    facebook=models.URLField(null=True, blank= True)
    Twitter=models.URLField(null=True, blank= True)
    

    def __str__(self):
        middle = f" {self.middle_name.capitalize()}" if self.middle_name else ""
        return f"{self.first_name.capitalize()}{middle} {self.last_name.capitalize()}"
    

class Booking(models.Model):
    created=models.DateField(auto_now_add=True)
    park = models.ForeignKey(Park, related_name='bookings', on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    message=models.TextField()
  
    def __str__(self):
        return f"{self.customer} - {self.park.name}"