from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from academics.models import Department, Program, University


class StudentApiTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="admin2", password="Admin@12345")
        self.student_user = user_model.objects.create_user(username="student1", password="Admin@12345")
        self.client.force_authenticate(self.user)

        self.university = University.objects.create(name="Sample University", code="SU")
        self.department = Department.objects.create(university=self.university, name="Computer Science", code="CS")
        self.program = Program.objects.create(department=self.department, name="BSCS", code="BSCS")

        self.university_2 = University.objects.create(name="Other University", code="OU")

    def test_create_student_profile(self):
        response = self.client.post(
            reverse("students-v1:student-profile-list"),
            {
                "user": self.student_user.id,
                "university": self.university.id,
                "program": self.program.id,
                "student_id": "STU-0001",
                "current_semester": 1,
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["student_id"], "STU-0001")

    def test_create_student_profile_rejects_program_from_other_university(self):
        response = self.client.post(
            reverse("students-v1:student-profile-list"),
            {
                "user": self.student_user.id,
                "university": self.university_2.id,
                "program": self.program.id,
                "student_id": "STU-0002",
                "current_semester": 1,
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("program", response.data)
