from django.core.management import BaseCommand
from users.models import User, Lessons, Course, Payments


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='users@sky.pro'
        )

        user.set_password('123')
        user.save()

        lesson_list = [
            {
                'title': 'Python lesson 1',
                'descriptions': 'Python 1'
            },
            {
                'title': 'Python lesson 2',
                'descriptions': 'Python 2'
            },
            {
                'title': 'JS les. 1',
                'descriptions': 'JS 1'
            }
        ]

        lessons = []
        for item in lesson_list:
            lessons.append(Lessons(**item))

        lessons_inter = Lessons.objects.bulk_create(lessons)

        course = Course.objects.create(
            title='Python developer',
            descriptions='Курсы по Python'
        )
        course.lessons.add(*lessons_inter[:2])
        course.save()

        Payments.objects.create(
            user=user,
            course=course,
            amount=150_000,
            payment_method='transfer'
        )

        Payments.objects.create(
            user=user,
            course=course,
            amount=10_000,
            payment_method='cash'
        )
