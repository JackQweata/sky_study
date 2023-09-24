from rest_framework import serializers

from users.models import Subscript


class LessonCustomValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        link = dict(value).get(self.field)
        if link.find('youtube.com') == -1:
            raise serializers.ValidationError('Ссылка неверна')

