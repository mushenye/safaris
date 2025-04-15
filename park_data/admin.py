from django.contrib import admin

from park_data.models import Accommodation, Booking, Park, ParkImage, ParkList

# Register your models here.
admin.site.register(Park)
admin.site.register(ParkList)
admin.site.register(Accommodation)
admin.site.register(ParkImage)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'created', 'park', 'short_message')
    list_filter = ('created', 'park')
    search_fields = ('customer__first_name', 'customer__last_name', 'park__name', 'message')

    def customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    customer_name.short_description = 'Customer'

    def short_message(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = 'Message'