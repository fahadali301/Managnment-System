from rest_framework.routers import DefaultRouter

from .views import EnrollmentViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register("profiles", StudentProfileViewSet, basename="student-profile")
router.register("enrollments", EnrollmentViewSet, basename="enrollment")

urlpatterns = router.urls

