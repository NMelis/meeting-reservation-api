import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
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


def test_register_user(api_client, db):
    url = reverse("register")
    data = {"username": "newuser", "password": "newpassword"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, response.json()



def test_login_user(api_client, user, db):
    url = reverse("token_obtain_pair")
    data = {"username": "testuser", "password": "testpassword"}
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "access" in response.data
