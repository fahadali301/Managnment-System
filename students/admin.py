from django.contrib import admin

from .models import Enrollment, StudentProfile


admin.site.register(StudentProfile)
admin.site.register(Enrollment)

