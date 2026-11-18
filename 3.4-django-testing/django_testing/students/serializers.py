from django.conf import settings
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_students(self, value):
        max_students = getattr(settings, 'MAX_STUDENTS_PER_COURSE', 20)
        if len(value) > max_students:
            raise serializers.ValidationError(
                f"Максимальное число студентов на курсе: {max_students}"
            )
        return value
