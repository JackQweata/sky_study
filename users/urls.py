from django.urls import path
from rest_framework import routers
from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonsListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonsDetailAPIView.as_view(), name='lesson-detail'),
    path('lessons/delete/<int:pk>/', LessonsDestroyAPIView.as_view(), name='lesson-delete'),
    path('lessons/update/<int:pk>/', LessonsUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/create/', LessonsCreateAPIView.as_view(), name='lesson-create'),
] + router.urls
