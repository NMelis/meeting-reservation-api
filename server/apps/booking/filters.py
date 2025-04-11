import django_filters
from .models import Room, Booking


class RoomFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(method='filter_available')
    start_time = django_filters.TimeFilter(method='filter_available')
    end_time = django_filters.TimeFilter(method='filter_available')
    capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')
    floor = django_filters.NumberFilter(field_name='floor')

    class Meta:
        model = Room
        fields = ['date', 'start_time', 'end_time', 'capacity', 'floor']

    def filter_available(self, queryset, name, value):
        date = self.data.get('date')
        start_time = self.data.get('start_time')
        end_time = self.data.get('end_time')

        if date and start_time and end_time:
            busy_rooms = Booking.objects.filter(
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).values_list('room_id', flat=True)

            return queryset.exclude(id__in=busy_rooms)
        return queryset
