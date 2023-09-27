from rest_framework import serializers
from users.models import Course, Lessons, Payments, Subscript
from users.tasks import updating_course_materials
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

    def update(self, instance, validated_data):
        if validated_data.get('title'):
            instance.title = validated_data['title']
        if validated_data.get('descriptions'):
            instance.descriptions = validated_data['descriptions']
        if validated_data.get('lessons'):
            instance.lessons.add(validated_data['lessons'])

        subscripts_users = Subscript.objects.filter(course=instance)
        user_emails = [user.owner.email for user in subscripts_users]
        updating_course_materials.delay(user_emails)

        instance.save()
        return instance


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['course', 'lesson', 'date', 'amount']
        extra_kwargs = {
            'course': {'required': False},
            'lesson': {'required': False},
            'date': {'required': False},
            'amount': {'required': False},
        }


class SubscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscript
        fields = '__all__'
        extra_kwargs = {'owner': {'required': False}, 'is_sub': {'required': False}}
