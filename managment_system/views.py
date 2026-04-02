from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from students.models import Enrollment, StudentProfile


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_students = StudentProfile.objects.count()
        active_students = StudentProfile.objects.filter(is_active=True).count()
        total_enrollments = Enrollment.objects.count()
        user_model = get_user_model()
        total_users = user_model.objects.count()

        context.update(
            {
                "total_students": total_students,
                "active_students": active_students,
                "total_enrollments": total_enrollments,
                "total_users": total_users,
            }
        )
        return context

