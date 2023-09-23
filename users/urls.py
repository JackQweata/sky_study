from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('lessons/', LessonsListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonsDetailAPIView.as_view(), name='lesson-detail'),
    path('lessons/delete/<int:pk>/', LessonsDestroyAPIView.as_view(), name='lesson-delete'),
    path('lessons/update/<int:pk>/', LessonsUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/create/', LessonsCreateAPIView.as_view(), name='lesson-create'),
    path('payment/', PaymentsListAPIView.as_view(), name='payment-list'),
] + router.urls
