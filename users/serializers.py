from rest_framework import serializers
from users.models import Course, Lessons, Payments, Subscript
from users.validators import LessonCustomValidator


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lessons
        fields = '__all__'
        extra_kwargs = {'owner': {'required': False}}
        validators = [LessonCustomValidator(field='link_video')]


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonsSerializer(many=True)
    is_sub = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_sub(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if Subscript.objects.filter(owner=user, course=obj).exists():
                return True
        return False

    def get_count_lesson(self, obj):
        return obj.lessons.count()


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscript
        fields = '__all__'
        extra_kwargs = {'owner': {'required': False}, 'is_sub': {'required': False}}
