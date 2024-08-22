from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Olympiad, OlympiadUser
from .serializers import OlympiadSerializer


class OlympiadListView(generics.ListAPIView):
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer


class OlympiadDetailView(generics.RetrieveAPIView):
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer


class OlympiadEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        olympiad = get_object_or_404(Olympiad, pk=pk)
        student = request.user
        result = olympiad.is_registrations_open()
        if result:
            if olympiad not in student.olympiad_set.all():
                OlympiadUser.objects.create(user=student, olympiad=olympiad, registration_date=datetime.now())

        return Response({'enrolled': True})
