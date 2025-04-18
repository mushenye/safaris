from datetime import date
from django.db import models
from django.utils import timezone
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

class Animal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    main_image = models.ImageField(upload_to='animal_profiles/')
    habitat_image1 = models.ImageField(upload_to='animal_profiles/', blank=True, null=True)
    habitat_image2 = models.ImageField(upload_to='animal_profiles/', blank=True, null=True)
    habitat_image3 = models.ImageField(upload_to='animal_profiles/', blank=True, null=True)

    def __str__(self):
        return self.name





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
    image = models.ImageField(upload_to='park_images/' ,blank=True)
    fee= models.DecimalField(max_digits=8, decimal_places=2, default=0.00 )
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    meal_cost= models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    contact_info = models.TextField()

    def __str__(self):
        return f"{self.hotel_name} in {self.park.name}"






    

class Customer (models.Model):
    created=models.DateField(auto_now_add=True)
    first_name= models.CharField(max_length=100)
    middle_name= models.CharField(max_length=100, blank=True, null=True)  
    last_name= models.CharField(max_length=100)
    id_or_passport= models.CharField(max_length=100, blank=True, null=True)
    country=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email=models.EmailField()
    facebook=models.URLField(null=True, blank= True)
    instagram=models.URLField(null=True, blank= True)
    Twitter=models.URLField(null=True, blank= True)
    
    

    def __str__(self):
        middle = f" {self.middle_name.capitalize()}" if self.middle_name else ""
        return f"{self.first_name.capitalize()}{middle} {self.last_name.capitalize()}"
    


class BookPark(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    created = models.DateTimeField(auto_now_add=True)
    park = models.ForeignKey('Park', related_name='bookings', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f'{self.customer} → {self.park.name} [{self.status.capitalize()}]'

    def is_due(self):
        return self.due_date >= timezone.now().date()



class TouringVan(models.Model):
    park = models.ForeignKey(Park, related_name='vans', on_delete=models.CASCADE)
    van_name = models.CharField(max_length=200)
    van_type = models.CharField(max_length=100, choices=[('4x4', '4x4'), ('Minibus', 'Minibus'), ('SUV', 'SUV')])
    seating_capacity = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    driver_included = models.BooleanField(default=True)
    image = models.ImageField(upload_to='van_images/', blank=True, null=True)
    contact_info = models.TextField()

    def __str__(self):
        return f"{self.van_name} ({self.van_type}) - {self.park.name}"


