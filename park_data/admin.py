from django.contrib import admin

from park_data.models import Accommodation, Park

# Register your models here.
admin.site.register(Park)
admin.site.register(Accommodation)