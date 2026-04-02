from rest_framework import permissions, viewsets

from .models import Course, Department, Program, Section, Term, University
from .serializer import (
    CourseSerializer,
    DepartmentSerializer,
    ProgramSerializer,
    SectionSerializer,
    TermSerializer,
    UniversitySerializer,
)


class BaseUniversityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]


class UniversityViewSet(BaseUniversityViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer


class DepartmentViewSet(BaseUniversityViewSet):
    queryset = Department.objects.select_related("university").all()
    serializer_class = DepartmentSerializer


class ProgramViewSet(BaseUniversityViewSet):
    queryset = Program.objects.select_related("department", "department__university").all()
    serializer_class = ProgramSerializer


class TermViewSet(BaseUniversityViewSet):
    queryset = Term.objects.select_related("university").all()
    serializer_class = TermSerializer


class CourseViewSet(BaseUniversityViewSet):
    queryset = Course.objects.select_related("program", "program__department").all()
    serializer_class = CourseSerializer


class SectionViewSet(BaseUniversityViewSet):
    queryset = Section.objects.select_related("course", "term").all()
    serializer_class = SectionSerializer

