import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from server.apps.booking.models import Room, Booking
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def room(db):
    return Room.objects.create(name="Room 101", capacity=10, floor=1)


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="otheruser", password="otherpassword")


@pytest.fixture
def auth_client():
    def _login(user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client
    return _login


@pytest.mark.django_db
def test_create_booking(auth_client, user, room):
    client = auth_client(user)
    url = reverse("booking-list")
    data = {
        "room": room.id,
        "date": (datetime.now() + timedelta(days=1)).date(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert response.data["room"] == room.id


@pytest.mark.django_db
def test_create_booking_conflict(auth_client, user, room):
    Booking.objects.create(
        user=user,
        room=room,
        date=(datetime.now() + timedelta(days=1)).date(),
        start_time="10:00",
        end_time="11:00"
    )
    client = auth_client(user)
    url = reverse("booking-list")
    data = {
        "room": room.id,
        "date": (datetime.now() + timedelta(days=1)).date(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_retrieve_booking(auth_client, user, room):
    booking = Booking.objects.create(
        user=user,
        room=room,
        date=(datetime.now() + timedelta(days=1)).date(),
        start_time="10:00",
        end_time="11:00"
    )
    client = auth_client(user)
    url = reverse("booking-detail", args=[booking.id])
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["room"] == room.id


@pytest.mark.django_db
def test_delete_booking(auth_client, user, room):
    booking = Booking.objects.create(
        user=user,
        room=room,
        date=(datetime.now() + timedelta(days=1)).date(),
        start_time="10:00",
        end_time="11:00"
    )
    client = auth_client(user)
    url = reverse("booking-detail", args=[booking.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Booking.objects.filter(id=booking.id).exists()


@pytest.mark.django_db
def test_user_can_only_see_own_bookings(auth_client, user, room):
    Booking.objects.create(
        user=user,
        room=room,
        date=(datetime.now() + timedelta(days=1)).date(),
        start_time="10:00",
        end_time="11:00"
    )
    client = auth_client(user)
    url = reverse("booking-list")
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_admin_can_see_all_bookings(auth_client, admin_user, user, room):
    Booking.objects.create(
        user=user,
        room=room,
        date=(datetime.now() + timedelta(days=1)).date(),
        start_time="10:00",
        end_time="11:00"
    )
    client = auth_client(admin_user)
    url = reverse("booking-list")
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


# @pytest.mark.django_db
# def test_user_can_only_update_own_booking(auth_client, user, admin_user, room):
#     booking = Booking.objects.create(
#         user=user,
#         room=room,
#         date=(datetime.now() + timedelta(days=1)).date(),
#         start_time="10:00",
#         end_time="11:00"
#     )
#     client_user = auth_client(user)
#     url = reverse("booking-detail", args=[booking.id])
#     data = {"start_time": "12:00", "end_time": "13:00"}
#     response = client_user.put(url, data, format="json")
#     assert response.status_code == status.HTTP_200_OK
#
#     client_admin = auth_client(admin_user)
#     data = {"start_time": "14:00", "end_time": "15:00"}
#     response = client_admin.put(url, data, format="json")
#     assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cannot_update_other_users_booking(auth_client, user, other_user, room):
    booking = Booking.objects.create(
        user=other_user,
        room=room,
        date=(datetime.now() + timedelta(days=1)).date(),
        start_time="10:00",
        end_time="11:00"
    )
    client = auth_client(user)
    url = reverse("booking-detail", args=[booking.id])
    data = {"start_time": "12:00", "end_time": "13:00"}
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_cannot_delete_other_users_booking(auth_client, user, other_user, room):
    booking = Booking.objects.create(
        user=other_user,
        room=room,
        date=(datetime.now() + timedelta(days=1)).date(),
        start_time="10:00",
        end_time="11:00"
    )
    client = auth_client(user)
    url = reverse("booking-detail", args=[booking.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_filter_rooms_by_date(auth_client, user, room):
    client = auth_client(user)
    url = reverse("room-list")
    response = client.get(url, {"date": (datetime.now() + timedelta(days=1)).date()})
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert len(response.data) == 1
