from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from users.models import Course, Lessons, Payments
from users.permissions import IsStaffOrOwner, IsOwner
from users.serializers import CourseSerializer, LessonsSerializer, PaymentsSerializer
from users.utils import ManagerRestrictionsMixin, OwnerProductsMixin


class CourseViewSet(OwnerProductsMixin, ManagerRestrictionsMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        new_curs = serializer.save()
        new_curs.owner = self.request.user
        new_curs.save()

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [IsStaffOrOwner]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]


class LessonsCreateAPIView(ManagerRestrictionsMixin, generics.CreateAPIView):
    serializer_class = LessonsSerializer

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonsUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsStaffOrOwner]
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDestroyAPIView(generics.DestroyAPIView):
    queryset = Lessons.objects.all()
    permission_classes = [IsOwner]


class LessonsListAPIView(OwnerProductsMixin, generics.ListAPIView):
    serializer_class = LessonsSerializer


class LessonsDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsStaffOrOwner]
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'payment_method')
    ordering_fields = ('date',)
