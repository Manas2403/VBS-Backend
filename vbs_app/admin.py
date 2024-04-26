from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Building)
admin.site.register(models.Venue)
admin.site.register(models.User)
admin.site.register(models.Booking)
admin.site.register(models.BookingRequest)
admin.site.register(models.Comments)
admin.site.register(models.VHVenue)
admin.site.register(models.VHBooking)
admin.site.register(models.VHBookingRequest)