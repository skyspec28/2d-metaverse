from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import CustomUser, Avatar, Space, Element, Map

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_user_login(self):
        # Create user first
        CustomUser.objects.create_user(**self.user_data)
        
        # Try logging in
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

class SpaceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create a test map
        self.map = Map.objects.create(
            name='Test Map',
            width=800,
            height=600,
            background_image='http://example.com/bg.png',
            tile_size=32
        )

    def test_create_space(self):
        url = reverse('space-create')
        data = {
            'name': 'Test Space',
            'width': 800,
            'height': 600,
            'map': self.map.id,
            'thumbnail': 'http://example.com/thumb.png'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Space.objects.filter(name='Test Space').exists())

    def test_list_spaces(self):
        # Create a test space
        Space.objects.create(
            name='Test Space',
            width=800,
            height=600,
            map=self.map,
            thumbnail='http://example.com/thumb.png'
        )
        
        url = reverse('space-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class ElementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_create_element(self):
        url = reverse('element-create')
        data = {
            'name': 'Test Chair',
            'type': 'furniture',
            'sprite_url': 'http://example.com/chair.png',
            'is_walkable': False,
            'interaction_script': 'console.log("Sitting")'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Element.objects.filter(name='Test Chair').exists()) 