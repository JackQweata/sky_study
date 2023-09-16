from django.contrib.auth.models import AbstractUser
from django.db import models

BLANCNULL = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email', unique=True)
    phone = models.CharField(**BLANCNULL, max_length=100, verbose_name='Телефон')
    cite = models.TextField(**BLANCNULL, verbose_name='город')
    avatar = models.ImageField(**BLANCNULL, upload_to="avatar_users/")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название курса')
    img = models.ImageField(**BLANCNULL, upload_to='courses/', verbose_name='Картинка')
    descriptions = models.TextField(**BLANCNULL, verbose_name='Описание')


class Lessons(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название урока')
    img = models.ImageField(**BLANCNULL, upload_to='lessons/', verbose_name='Картинка')
    link_video = models.CharField(**BLANCNULL, max_length=255, verbose_name='Ссылка на видео')
    descriptions = models.TextField('Описание')
