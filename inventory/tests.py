from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import InventoryItem

class InventoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('bob','bob@example.com','pass')
        self.client.login(username='bob', password='pass')

    def test_create_item(self):
        data = {"name":"A","dose":"10mg","quantity":5,"price":"1.00"}
        resp = self.client.post('/api/drugs/', data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(InventoryItem.objects.count(), 1)
