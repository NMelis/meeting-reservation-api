from rest_framework import serializers
from .models import Room, Booking
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()



class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'capacity', 'floor')


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'capacity', 'floor')


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


    class Meta:
        model = Booking
        fields = ('id', 'room', 'user', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)

    def save(self, **kwargs):
        request = self.context['request']
        if request.user.is_staff:
            user = kwargs.get('user') or request.user
        else:
            user = request.user
        kwargs['user'] = user

    def validate(self, data):
        request = self.context['request']
        if request.user.is_staff:
            user = data.get('user') or request.user
        else:
            user = request.user

        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        room = data.get('room')

        if not all([date, start_time, end_time, room]):
            return data

        user_bookings = Booking.objects.filter(user=user, date=date)
        for booking in user_bookings:
            if start_time < booking.end_time and end_time > booking.start_time:
                raise serializers.ValidationError(_("Вы уже забронировали комнату в это время."))

        room_bookings = Booking.objects.filter(room=room, date=date)
        for booking in room_bookings:
            if start_time < booking.end_time and end_time > booking.start_time:
                raise serializers.ValidationError(_("Комната уже забронирована в это время."))

        return data
