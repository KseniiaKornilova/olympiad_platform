from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegistrationsSerializer, UserProfileSerializer
from drf_yasg.utils import swagger_auto_schema


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register user",
        responses={
            200: "Вы успешно зарегистрированы",
            400: "При регистрации произошла ошибка"
        }
    )
    def post(self, request, format=None):
        serializer = UserRegistrationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Вы успешно зарегистрированы"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change user's data",
        responses={
            200: "Данные Вашего профиля успешно изменены",
            400: "При изменении данных произошла ошибка"
        }
    )
    def put(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Данные Вашего профиля успешно изменены"},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
