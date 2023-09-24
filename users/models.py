from django.contrib.auth.models import AbstractUser
from django.db import models

BLANCNULL = {'blank': True, 'null': True}

PAYMENT_METHOD = (
    ('cash', 'наличные'),
    ('transfer', 'перевод')
)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email', unique=True)
    phone = models.CharField(**BLANCNULL, max_length=100, verbose_name='Телефон')
    cite = models.TextField(**BLANCNULL, verbose_name='город')
    avatar = models.ImageField(**BLANCNULL, upload_to="avatar_users/")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Lessons(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    img = models.ImageField(**BLANCNULL, upload_to='lessons/', verbose_name='Картинка')
    link_video = models.CharField(**BLANCNULL, max_length=255, verbose_name='Ссылка на видео')
    descriptions = models.TextField('Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Course(models.Model):
    lessons = models.ManyToManyField(Lessons, related_name='lessons', **BLANCNULL)

    title = models.CharField(max_length=100, verbose_name='Название курса')
    img = models.ImageField(**BLANCNULL, upload_to='courses/', verbose_name='Картинка')
    descriptions = models.TextField(**BLANCNULL, verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **BLANCNULL, related_name='course')
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, **BLANCNULL, related_name='lesson')

    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)


class Subscript(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_sub = models.BooleanField(**BLANCNULL)
