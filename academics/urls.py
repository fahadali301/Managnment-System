from rest_framework.routers import DefaultRouter

from .views import (
    CourseViewSet,
    DepartmentViewSet,
    ProgramViewSet,
    SectionViewSet,
    TermViewSet,
    UniversityViewSet,
)

router = DefaultRouter()
router.register("universities", UniversityViewSet, basename="university")
router.register("departments", DepartmentViewSet, basename="department")
router.register("programs", ProgramViewSet, basename="program")
router.register("terms", TermViewSet, basename="term")
router.register("courses", CourseViewSet, basename="course")
router.register("sections", SectionViewSet, basename="section")

urlpatterns = router.urls
