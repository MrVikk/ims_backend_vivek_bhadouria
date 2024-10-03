from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
class ItemTests(APITestCase):
    def setUp(self):
        self.item = Item.objects.create(name='Item 1', description='Description 1', quantity=10, price=50)
        self.token = self.get_jwt_token()

    def get_jwt_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'admin', 'password': 'password'})
        return response.data['access']

    def test_get_items(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('item_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_item(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        url = reverse('item_list_create')
        data = {'name': 'Item 2', 'description': 'Description 2', 'quantity': 5, 'price': 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)