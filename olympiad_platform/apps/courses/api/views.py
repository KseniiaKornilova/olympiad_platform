from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsEnrolledOrAdmin
from .serializers import CourseSerializer, LessonSerializer
from ..models import Assignment, AssignmentSubmission, Course, CourseUser, Lesson


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(
        operation_description="Enroll a user in the course",
        responses={
            200: "Вы успешно зарегистрированы",
            400: "Вы являетесь преподавателем на данном курсе",
            409: "Вы уже зарегистрированы на данный курс"
        }
    )
    @action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        course_teacher = course.teacher
        if user != course_teacher:
            if CourseUser.objects.filter(user=user, course=course).exists():
                return Response({
                    'enrolled': False,
                    'message': 'Вы уже зарегистрированы на данный курс'
                }, status=status.HTTP_409_CONFLICT)
            else:
                CourseUser.objects.create(user=user, course=course)
                assignments = Assignment.objects.filter(course=course)
                for assignment in assignments:
                    AssignmentSubmission.objects.create(assignment=assignment, student=user)
                return Response({
                    'enrolled': True,
                    'message': 'Вы успешно зарегистрированы'
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'enrolled': False,
                'message': 'Вы являетесь преподавателем на данном курсе'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsEnrolledOrAdmin])
    def lessons(self, request, *args, **kwargs):
        course = self.get_object()
        lessons = Lesson.objects.filter(course=course)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Unenroll a user from the course",
        responses={
            200: "Вы успешно отписались от курса",
            403: "Вы не являлись участником курса"
        }
    )
    @action(detail=True, methods=['delete'], authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def stop_course(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        course_user = CourseUser.objects.filter(user=user, course=course)

        if course_user.exists():
            course_user.delete()
            return Response({
                    'deleted': True,
                    'message': 'Вы успешно отписались от курса'
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                    'deleted': False,
                    'message': 'Вы не являлись участником курса'
                }, status=status.HTTP_403_FORBIDDEN)
