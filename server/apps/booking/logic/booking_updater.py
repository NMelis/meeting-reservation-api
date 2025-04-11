from dataclasses import dataclass
from server.apps.booking.models import Booking
from django.utils.translation import gettext_lazy as _


@dataclass
class BookingUpdater:
    booking: 'Booking'
    user: 'User'
    room: 'Room'
    date: 'DateField'
    start_time: 'TimeField'
    end_time: 'TimeField'

    def __call__(self):
        self._check_user_booking()
        self._check_room_booking()

        self.booking.room = self.room
        self.booking.date = self.date
        self.booking.start_time = self.start_time
        self.booking.end_time = self.end_time
        self.booking.save()

        return self.booking

    def _check_user_booking(self):
        user_bookings = Booking.objects.filter(
            user=self.user,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        if user_bookings.exists():
            raise ValueError(_("Вы уже забронировали комнату в это время."))

    def _check_room_booking(self):
        room_bookings = Booking.objects.filter(
            room=self.room,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )

        if room_bookings.exists():
            raise ValueError(_("Комната уже забронирована в это время."))
