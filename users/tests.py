from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Lessons, User, Subscript, Course


class LessonsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="users@sky.pro",
            password="123"
        )

        self.lesson_data = {
            'title': 'Test Lesson 1',
            'descriptions': 'test',
            'link_video': 'youtube.com',
            'owner': self.user.pk
        }
        self.access_token = self.get_access_token()

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_create_lesson(self):
        """ Test creating a new lesson """
        response = self.client.post(
            '/api/lessons/create/',
            self.lesson_data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lessons.objects.count(), 1)

    def test_get_lesson(self):
        """ Test retrieving a lesson """
        self.lesson_data['owner'] = self.user
        lesson = Lessons.objects.create(**self.lesson_data)
        response = self.client.get(f'/api/lessons/{lesson.id}/', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), lesson.title)

    def test_update_lesson(self):
        """ Test updating a lesson """
        self.lesson_data['owner'] = self.user
        lesson = Lessons.objects.create(**self.lesson_data)
        updated_data = {
            'title': 'Updated Lesson',
            'descriptions': 'updated lesson',
            'link_video': 'youtube.com'
        }
        response = self.client.put(
            f'/api/lessons/update/{lesson.id}/',
            updated_data, HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), updated_data['title'])
        self.assertEqual(response.data.get('descriptions'), updated_data['descriptions'])

    def test_delete_lesson(self):
        """ Test deleting a lesson """
        self.lesson_data['owner'] = self.user
        lesson = Lessons.objects.create(**self.lesson_data)
        response = self.client.delete(
            f'/api/lessons/delete/{lesson.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lessons.objects.count(), 0)


class SubscriptTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="users@sky.pro",
            password="123"
        )

        self.course = Course.objects.create(title="Test course", owner=self.user)

        self.access_token = self.get_access_token()

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        return str(refresh.access_token)

    def test_create_subscript(self):
        """ Test creating a new subscript """
        data = {"course": 1}
        response = self.client.post(
            '/api/subscript/create/',
            data,
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscript.objects.count(), 1)

    def test_delete_subscript(self):
        """ Test deleting a subscript """

        subscript = Subscript.objects.create(owner=self.user, course=self.course, is_sub=True)

        response = self.client.delete(
            f'/api/subscript/delete/{subscript.id}/',
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscript.objects.count(), 0)
