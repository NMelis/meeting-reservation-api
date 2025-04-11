from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from server.apps.booking.models import Booking, Room


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'date', 'start_time', 'end_time')
    list_filter = ('date', 'room', 'user')
    search_fields = ('user__username', 'room__name')
    ordering = ('-date',)
    date_hierarchy = 'date'

    fieldsets = (
        (None, {'fields': ('user', 'room', 'date', 'start_time', 'end_time')}),
    )


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor', 'capacity')
    search_fields = ('name', 'floor')
    list_filter = ('floor', 'capacity')
