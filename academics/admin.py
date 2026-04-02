from django.contrib import admin

from .models import Course, Department, Program, Section, Term, University


admin.site.register(University)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(Term)
admin.site.register(Course)
admin.site.register(Section)

