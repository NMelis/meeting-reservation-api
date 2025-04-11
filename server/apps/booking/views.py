from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from .filters import RoomFilter
from .logic.booking_creator import BookingCreator
from .logic.booking_updater import BookingUpdater
from .models import Room, Booking
from .serializers import RoomSerializer, RoomDetailSerializer, BookingSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoomDetailSerializer
        return RoomSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.validated_data
        BookingCreator(
            user=data.get('user', self.request.user),
            room=data['room'],
            date=data['date'],
            start_time=data['start_time'],
            end_time=data['end_time']
        )()

    def perform_update(self, serializer):
        booking = self.get_object()
        data = serializer.validated_data
        BookingUpdater(
            booking=booking,
            user=data.get('user', self.request.user),
            room=data['room'],
            date=data['date'],
            start_time=data['start_time'],
            end_time=data['end_time']
        )()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
