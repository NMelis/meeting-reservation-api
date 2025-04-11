from dataclasses import dataclass
from django.utils.translation import gettext_lazy as _
from server.apps.booking.models import Booking


@dataclass
class BookingCreator:
    user: 'User'
    room: 'Room'
    date: 'DateField'
    start_time: 'TimeField'
    end_time: 'TimeField'

    def __call__(self, *args, **kwargs):
        self._check_user_booking()
        self._check_room_booking()

        booking = Booking.objects.create(
            user=self.user,
            room=self.room,
            date=self.date,
            start_time=self.start_time,
            end_time=self.end_time,
        )
        return booking

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



