from apps.students.api.serializers import UserSerializer

from rest_framework import serializers

from ..models import Olympiad


class OlympiadSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Olympiad
        fields = '__all__'
