from rest_framework import serializers
from ..models import Course, Lesson
from apps.students.api.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
