from django.db import models

class Park(models.Model):
    country = models.CharField(max_length=100)
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=255, help_text="Nearest city or coordinates")
    established_date = models.DateField(null=True, blank=True)
    size_sq_km = models.FloatField(null=True, blank=True, help_text="Size in square kilometers")
    description = models.TextField( )
    history = models.TextField()
    flora_and_fauna = models.TextField(help_text="Details about wildlife and plants seen at the park")
    climate = models.TextField(blank=True, help_text="Weather and best time to visit")
    booking_info = models.TextField(help_text="How visitors can book or contact you")

    def __str__(self):
        return self.name
    
    
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

