from django.conf import settings
from django.db import models

from academics.models import Program, Section, University


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    university = models.ForeignKey(University, on_delete=models.PROTECT, related_name="students")
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name="students")
    student_id = models.CharField(max_length=30, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    current_semester = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["student_id"]

    def __str__(self) -> str:
        return f"{self.student_id} - {self.user.username}"


class Enrollment(models.Model):
    STATUS_CHOICES = (
        ("enrolled", "Enrolled"),
        ("dropped", "Dropped"),
        ("completed", "Completed"),
    )

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="enrollments")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="enrolled")
    final_grade = models.CharField(max_length=5, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-enrolled_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "section"], name="uniq_student_section_enrollment"),
        ]

    def __str__(self) -> str:
        return f"{self.student.student_id} -> {self.section}"

