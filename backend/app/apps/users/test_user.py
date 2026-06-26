from django.urls import reverse

import pytest
from apps.users.models import User


@pytest.mark.django_db
def test_register_success(client):
    user_data = {
        "username": "testuser",
        "password1": "Testpass123!",
        "password2": "Testpass123!",
    }

    response = client.post("/users/signup/", user_data)

    assert response.status_code == 302
    assert response.url == "/"

    assert User.objects.filter(
        username=user_data["username"]
    ).exists()


@pytest.mark.django_db
def test_login_success(client):
    User.objects.create_user(
        username="TestUser12345",
        password="qazwsxedcrfvtgb1234567890"
    )

    response = client.post(
        reverse("login"),
        {
            "username": "TestUser12345",
            "password": "qazwsxedcrfvtgb1234567890",
        }
    )

    assert response.status_code == 302
    assert response.url == reverse("index")


def test_regular_user_cannot_access_crud_shop(client, regular_user):
    client.force_login(regular_user)

    response = client.get(reverse("crud_shops"))

    assert response.status_code == 302
    assert response.url == f"{reverse('user_redirect')}?next={reverse('crud_shops')}"


def test_regular_user_cannot_access_crud_users(client, regular_user):
    client.force_login(regular_user)

    response = client.get(reverse("crud_users"))

    assert response.status_code == 302
    assert response.url == f"{reverse('user_redirect')}?next={reverse('crud_users')}"
