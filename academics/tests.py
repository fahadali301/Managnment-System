from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AcademicsApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="admin1", password="Admin@12345")
        self.client.force_authenticate(self.user)

    def test_create_university(self):
        response = self.client.post(
            reverse("academics-v1:university-list"),
            {"name": "Sample University", "code": "SU", "address": "Main Street"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["code"], "SU")
