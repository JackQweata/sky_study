from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from users.models import Course, Lessons, Payments, Subscript
from users.paginations import ListProductsPagination
from users.permissions import IsStaffOrOwner, IsOwner
from users.serializers import CourseSerializer, LessonsSerializer, PaymentsSerializer, SubscriptSerializer
from users.utils import ManagerRestrictionsMixin, OwnerProductsMixin
from rest_framework.permissions import AllowAny


class CourseViewSet(OwnerProductsMixin, ManagerRestrictionsMixin, viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = ListProductsPagination
    ordering_fields = ('title',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        permission_classes = []

        if self.action == 'retrieve':
            permission_classes = [IsStaffOrOwner]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]


class LessonsCreateAPIView(ManagerRestrictionsMixin, generics.CreateAPIView):
    serializer_class = LessonsSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonsUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsStaffOrOwner]
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDestroyAPIView(generics.DestroyAPIView):
    queryset = Lessons.objects.all()
    permission_classes = [IsOwner]


class LessonsListAPIView(generics.ListAPIView):
    queryset = Lessons.objects.all().order_by('title')
    serializer_class = LessonsSerializer
    pagination_class = ListProductsPagination


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


class SubscriptCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptSerializer

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data['course']

        if Subscript.objects.filter(owner=user, course=course).exists():
            raise ValidationError('Уже подписан')

        serializer.save(owner=self.request.user, is_sub=True)


class SubscriptDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscript.objects.all()
    permission_classes = [IsOwner]
