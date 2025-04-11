from typing import final, Final

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

#: That's how constants should be defined.
_POST_TITLE_MAX_LENGTH: Final = 80
User = get_user_model()


@final
class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    floor = models.IntegerField()

    def __str__(self):
        return _("%(name)s (этаж %(floor)d, %(capacity)d чел.)") % {
            "name": self.name,
            "floor": self.floor,
            "capacity": self.capacity,
        }


@final
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('room', 'date', 'start_time', 'end_time')

    def __str__(self):
        return _(
            "%(room)s забронирована %(user)s на %(date)s с %(start)s до %(end)s"
        ) % {
            "room": self.room.name,
            "user": self.user.username,
            "date": self.date,
            "start": self.start_time,
            "end": self.end_time,
        }
