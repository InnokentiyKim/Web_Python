import pytest
from rest_framework.test import APIClient


PRODUCTS_URL = "/api/v1/products/"


@pytest.mark.django_db
def test_products():
    client = APIClient()
    response = client.get(PRODUCTS_URL)
    assert response.status_code == 200
