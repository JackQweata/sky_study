from rest_framework import viewsets, generics
from users.models import Course, Lessons
from users.serializers import CourseSerializer, LessonsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonsCreateAPIView(generics.CreateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsUpdateAPIView(generics.UpdateAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDestroyAPIView(generics.DestroyAPIView):
    queryset = Lessons.objects.all()


class LessonsListAPIView(generics.ListAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDetailAPIView(generics.RetrieveAPIView):
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer
