from rest_framework import serializers
from ..models import Olympiad
from apps.students.api.serializers import UserSerializer


class OlympiadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Olympiad
        fields = '__all__'
