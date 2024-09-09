from datetime import datetime

from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import OlympiadSerializer
from ..models import Olympiad, OlympiadUser


class OlympiadListView(generics.ListAPIView):
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer


class OlympiadDetailView(generics.RetrieveAPIView):
    queryset = Olympiad.objects.all()
    serializer_class = OlympiadSerializer


class OlympiadEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Enroll a user in the olympiad",
        responses={
            200: "Вы успешно зарегистрированы",
            409: "Вы уже зарегистрированы на данную олимпиаду",
            410: "Регистрация на олимпиаду уже завершена"
        }
    )
    def post(self, request, pk, format=None):
        olympiad = get_object_or_404(Olympiad, pk=pk)
        student = request.user
        result = olympiad.is_registrations_open()
        if result:
            if olympiad not in student.olympiad_set.all():
                OlympiadUser.objects.create(user=student, olympiad=olympiad, registration_date=datetime.now())

                return Response({
                            'enrolled': True,
                            'message': 'Вы успешно зарегистрированы'
                        }, status=status.HTTP_200_OK)
            else:
                return Response({
                            'enrolled': False,
                            'message': 'Вы уже зарегистрированы на данную олимпиаду'
                        }, status=status.HTTP_409_CONFLICT)
        else:
            return Response({
                            'enrolled': False,
                            'message': 'Вы уже зарегистрированы на данную олимпиаду'
                            }, status=status.HTTP_410_GONE)


class OlympiadUnenrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Unenroll a user from the olympiad",
        responses={
            200: "Вы успешно отписались от олимпиады",
            403: "Вы не были зарегистрированы на данную олимпиаду"
        }
    )
    def delete(self, request, pk, format=None):
        olympiad = get_object_or_404(Olympiad, pk=pk)
        student = request.user
        olympiad_user = OlympiadUser.objects.filter(user=student, olympiad=olympiad)

        if olympiad_user.exists():
            olympiad_user.delete()
            return Response({
                'deleted': True,
                'message': 'Вы успешно отписались от олимпиады'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'deleted': False,
                'message': 'Вы не были зарегистрированы на данную олимпиаду'
            }, status=status.HTTP_403_FORBIDDEN)
