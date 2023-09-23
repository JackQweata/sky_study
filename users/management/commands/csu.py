from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from users.models import User, Lessons, Course, Payments


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='users@sky.pro'
        )

        user.set_password('123')
        user.save()

        manager = User.objects.create(
            email='manager@sky.pro',
            is_staff=True
        )

        group, create = Group.objects.get_or_create(name='manager')

        lessons = ContentType.objects.get_for_model(Lessons)
        courses = ContentType.objects.get_for_model(Course)
        user = ContentType.objects.get_for_model(User)

        perm_change_lessons = Permission.objects.get(codename='change_lessons', content_type=lessons)
        perm_view_lessons = Permission.objects.get(codename='view_lessons', content_type=lessons)

        perm_view_courses = Permission.objects.get(codename='view_course', content_type=courses)
        perm_change_courses = Permission.objects.get(codename='change_course', content_type=courses)

        perm_change_user = Permission.objects.get(codename='change_user', content_type=user)
        perm_view_user = Permission.objects.get(codename='view_user', content_type=user)

        group.permissions.add(
            perm_change_lessons,
            perm_view_lessons,
            perm_change_user,
            perm_view_user,
            perm_view_courses,
            perm_change_courses
        )

        manager.groups.add(group)
        manager.set_password('123')
        manager.save()

        lesson_list = [
            {
                'title': 'Python lesson 1',
                'descriptions': 'Python 1',
                'owner': User.objects.get(pk=1)
            },
            {
                'title': 'Python lesson 2',
                'descriptions': 'Python 2',
                'owner': User.objects.get(pk=1)
            },
            {
                'title': 'JS les. 1',
                'descriptions': 'JS 1',
                'owner': User.objects.get(pk=2)
            }
        ]

        lessons = []
        for item in lesson_list:
            lessons.append(Lessons(**item))

        lessons_inter = Lessons.objects.bulk_create(lessons)

        course = Course.objects.create(
            title='Python developer',
            descriptions='Курсы по Python',
            owner=User.objects.get(pk=1)
        )
        course.lessons.add(*lessons_inter[:2])
        course.save()

        Payments.objects.create(
            user=User.objects.get(pk=1),
            course=course,
            amount=150_000,
            payment_method='transfer'
        )

        Payments.objects.create(
            user=User.objects.get(pk=1),
            course=course,
            amount=10_000,
            payment_method='cash'
        )
