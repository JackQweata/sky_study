import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from users.models import Course, Lessons, Payments, Subscript
from users.paginations import ListProductsPagination
from users.permissions import IsStaffOrOwner, IsOwner
from users.serializers import CourseSerializer, LessonsSerializer, PaymentsSerializer, SubscriptSerializer
from users.services import get_payment_url
from users.utils import ManagerRestrictionsMixin, OwnerProductsMixin


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
    """ Endpoint for creating a lesson  """

    serializer_class = LessonsSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonsUpdateAPIView(generics.UpdateAPIView):
    """ Endpoint for update a lesson  """

    permission_classes = [IsStaffOrOwner]
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class LessonsDestroyAPIView(generics.DestroyAPIView):
    """ Endpoint for delete a lesson  """

    queryset = Lessons.objects.all()
    permission_classes = [IsOwner]


class LessonsListAPIView(generics.ListAPIView):
    """ Endpoint for viewing all lessons  """

    queryset = Lessons.objects.all().order_by('title')
    serializer_class = LessonsSerializer
    pagination_class = ListProductsPagination


class LessonsDetailAPIView(generics.RetrieveAPIView):
    """ Endpoint for viewing a detailed lesson """

    permission_classes = [IsStaffOrOwner]
    queryset = Lessons.objects.all()
    serializer_class = LessonsSerializer


class PaymentsListAPIView(generics.ListAPIView):
    """ List of all payment transactions """

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson', 'payment_method')
    ordering_fields = ('date',)


class SubscriptCreateAPIView(generics.CreateAPIView):
    """ Creating a subscription for a user for a course """

    serializer_class = SubscriptSerializer

    def perform_create(self, serializer):
        user = self.request.user
        course = serializer.validated_data['course']

        if Subscript.objects.filter(owner=user, course=course).exists():
            raise ValidationError('Уже подписан')

        serializer.save(owner=self.request.user, is_sub=True)


class SubscriptDestroyAPIView(generics.DestroyAPIView):
    """ Deleting a subscription for a user for a course """

    queryset = Subscript.objects.all()
    permission_classes = [IsOwner]


class PayCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get('course'):
            product = serializer.validated_data.get('course')

        elif serializer.validated_data.get('lesson'):
            product = serializer.validated_data.get('lesson')

        else:
            raise ValidationError('не указан course или lesson')

        session = get_payment_url(product)

        serializer.save(
            user=self.request.user,
            payment_id=session.id,
            amount=product.price,
            payment_method='transfer'
        )
        return Response({"date": session.url})


# class PayRetrieveAPIView(generics.RetrieveAPIView):
#     pass
