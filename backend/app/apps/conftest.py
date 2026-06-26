import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def regular_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="regular_user",
        password="testpass12345",
        first_name="Regular",
        last_name="User",
        patronymic="Test",
        document_in_passport="AA123456",
        nn_in_passport="1234567890",
    )