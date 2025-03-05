import pytest
from api.models import Avatar
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
class TestAvatarRetrieveView:
    def setup_method(self):
        self.client=APIClient()
        self.avatar=Avatar.objects.create(name="Test Avatar",image_url="https://example.com")
        self.valid_url= f"/api/v1/avatars/{self.avatar.pk}/"
        self.invalid_url= "/api/v1/avatars/999/"


        # test_retrieve_valid_avatar

    def test_retrieve_valid_avatar(self):
        response=self.client.get(self.valid_url)
        assert response.status_code== status.HTTP_200_OK
        assert response.data["name"] == "Test Avatar"
        assert response.data["image_url"] == "https://example.com"


        # test_invalid_avatar
    def test_retrieve_non_existent_avatar(self):
        response=self.client.get(self.invalid_url)
        assert response.status_code== status.HTTP_404_NOT_FOUND
        # test_valid_method

    def test_invalid_method(self):
        response=self.client.post(self.valid_url)
        assert response.status_code== status.HTTP_405_METHOD_NOT_ALLOWED