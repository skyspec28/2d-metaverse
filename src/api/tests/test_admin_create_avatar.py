import pytest
from api.models import Avatar
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User



@pytest.mark.django_db
class TestAdminCreateAvatarView:
    def setup_method(self):
        self.client=APIClient()
        self.avatar_data = {
            "image_url": "https://example.com",
            "name": "mario"
        }
        self.valid_url = "/api/v1/admin/avatar/new/"
    
    def test_admin_creates_avatar(self):
        response=self.client.post(self.valid_url ,self.avatar_data , format="json")
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()  
        assert response_data["message"] == "created successfully"  # Message check
        assert "avatar_id" in response_data  # Ensure avatar_id is in response
        assert Avatar.objects.filter(name="mario").exists()
        avatar = Avatar.objects.get(id=response_data["avatar_id"])
        assert avatar.name == "mario"
        assert avatar.image_url == "https://example.com"

    