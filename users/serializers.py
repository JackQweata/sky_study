from rest_framework import serializers
from users.models import Course, Lessons, Payments


class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessons
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonsSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, obj):
        return obj.lessons.count()


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
