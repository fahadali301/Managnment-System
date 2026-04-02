from rest_framework import serializers

from .models import Enrollment, StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"

    def validate(self, attrs):
        university = attrs.get("university")
        program = attrs.get("program")

        if university and program and program.department.university_id != university.id:
            raise serializers.ValidationError(
                {"program": "Selected program does not belong to the selected university."}
            )

        return attrs


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"

    def validate(self, attrs):
        section = attrs.get("section")
        current_instance = self.instance

        if section:
            enrolled_count = section.enrollments.filter(status="enrolled")
            if current_instance:
                enrolled_count = enrolled_count.exclude(pk=current_instance.pk)
            if enrolled_count.count() >= section.capacity:
                raise serializers.ValidationError({"section": "Section capacity is full."})

        return attrs
