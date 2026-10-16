import pytest
from django.db.models import Avg

from apps.users.models import Review, Shop, User


@pytest.mark.django_db
def test_average_rating():
    shop = Shop.objects.create(
        title="Comfy Test",
        description="Test description",
    )

    first_user = User.objects.create_user(
        username="first_user",
        email="first@example.com",
        password="testpass123",
    )

    second_user = User.objects.create_user(
        username="second_user",
        email="second@example.com",
        password="testpass123",
    )

    Review.objects.create(
        shop=shop,
        user=first_user,
        rating=5,
        comment="Good shop",
    )

    Review.objects.create(
        shop=shop,
        user=second_user,
        rating=1,
        comment="Bad shop",
    )

    reviews = Review.objects.filter(shop=shop)

    average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    reviews_count = reviews.count()

    assert average_rating == 3
    assert reviews_count == 2
