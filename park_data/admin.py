from django.contrib import admin

from park_data.models import Accommodation, Animal, Customer, Park, ParkImage, ParkList, TouringVan, Catalog

# Register your models here.
admin.site.register(Park)
admin.site.register(ParkList)
admin.site.register(Accommodation)
admin.site.register(ParkImage)
admin.site.register(Animal)
admin.site.register(Customer)
admin.site.register(Catalog)




# @admin.register(BookPark)
# class BookParkAdmin(admin.ModelAdmin):
#     list_display = ('customer','due_date' ,'park', 'status', 'created')
#     list_filter = ('status', 'created', 'park')
#     search_fields = ('customer__first_name', 'customer__last_name', 'park__name')
#     def customer_name(self, obj):
#         return f"{obj.customer.first_name} {obj.customer.last_name}"
#     customer_name.short_description = 'Customer'

#     def short_message(self, obj):
#         return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
#     short_message.short_description = 'Message'


@admin.register(TouringVan)
class TouringVanAdmin(admin.ModelAdmin):
    list_display = ('van_name', 'van_type', 'daily_rate','driver_included', 'availability')
    list_filter = ('van_type','availability')
    search_fields = ('van_name', 'van_type')