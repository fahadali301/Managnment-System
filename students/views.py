from rest_framework import permissions, viewsets

from .models import Enrollment, StudentProfile
from .serializer import EnrollmentSerializer, StudentProfileSerializer


class BaseStudentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class StudentProfileViewSet(BaseStudentViewSet):
    queryset = StudentProfile.objects.select_related("user", "university", "program").all()
    serializer_class = StudentProfileSerializer


class EnrollmentViewSet(BaseStudentViewSet):
    queryset = Enrollment.objects.select_related("student", "section", "section__course", "section__term").all()
    serializer_class = EnrollmentSerializer

