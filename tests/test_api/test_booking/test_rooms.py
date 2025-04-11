import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from server.apps.booking.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username="adminuser", password="adminpassword")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def room(admin_user, db):
    return Room.objects.create(name="Room 101", capacity=10, floor=1)


@pytest.fixture
def get_token(api_client):
    def _get_token(username, password):
        url = reverse("token_obtain_pair")
        response = api_client.post(url, {"username": username, "password": password}, format="json")
        assert response.data.get("access"), response.json()
        return response.data["access"]
    return _get_token


@pytest.fixture
def auth_client(api_client, get_token):
    def _auth_client(username, password):
        token = get_token(username, password)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return api_client
    return _auth_client


@pytest.mark.django_db
def test_create_room_as_admin(admin_user, auth_client):
    client = auth_client("adminuser", "adminpassword")
    url = reverse("room-list")
    data = {"name": "Room 102", "capacity": 15, "floor": 2}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Room 102"


@pytest.mark.django_db
def test_create_room_as_non_admin(user, auth_client):
    client = auth_client("testuser", "testpassword")
    url = reverse("room-list")
    data = {"name": "Room 103", "capacity": 20, "floor": 3}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_retrieve_room(room, user, auth_client):
    client = auth_client("testuser", "testpassword")
    url = reverse("room-detail", args=[room.id])
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == room.name


@pytest.mark.django_db
def test_update_room_as_admin(admin_user, auth_client, room):
    client = auth_client("adminuser", "adminpassword")
    url = reverse("room-detail", args=[room.id])
    data = {"name": "Updated Room", "capacity": 20, "floor": 2}
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Updated Room"


@pytest.mark.django_db
def test_update_room_as_non_admin(user, auth_client, room):
    client = auth_client("testuser", "testpassword")
    url = reverse("room-detail", args=[room.id])
    data = {"name": "Updated Room", "capacity": 20, "floor": 2}
    response = client.put(url, data, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_delete_room_as_admin(admin_user, auth_client, room):
    client = auth_client("adminuser", "adminpassword")
    url = reverse("room-detail", args=[room.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Room.objects.filter(id=room.id).exists()


@pytest.mark.django_db
def test_delete_room_as_non_admin(user, auth_client, room):
    client = auth_client("testuser", "testpassword")
    url = reverse("room-detail", args=[room.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
