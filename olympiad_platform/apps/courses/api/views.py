from ..models import Course, CourseUser, Assignment, AssignmentSubmission, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsEnrolledOrAdmin
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        user = request.user
        course_teacher = course.teacher
        if user != course_teacher:
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
