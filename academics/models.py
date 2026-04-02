from django.db import models


class University(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="departments")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["university", "code"], name="uniq_department_code_per_university"),
        ]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Program(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="programs")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    duration_years = models.PositiveSmallIntegerField(default=4)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["department", "code"], name="uniq_program_code_per_department"),
        ]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Term(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name="terms")
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(fields=["university", "name"], name="uniq_term_name_per_university"),
        ]

    def __str__(self) -> str:
        return self.name


class Course(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    credit_hours = models.PositiveSmallIntegerField(default=3)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(fields=["program", "code"], name="uniq_course_code_per_program"),
        ]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=40)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["course", "term", "name"], name="uniq_section_name_per_course_term"),
        ]

    def __str__(self) -> str:
        return f"{self.course.code}-{self.name} ({self.term.name})"

