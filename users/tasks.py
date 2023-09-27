import smtplib
from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail

from config import settings
from users.models import User


@shared_task
def updating_course_materials(user_emails):
    for item in user_emails:
        send_mail('Обновление', f'Привет! Курс обновился, заходи на сайт!',
                  settings.EMAIL_HOST_USER, [item], fail_silently=True)


@shared_task
def users_inactive():
    cutoff_date = datetime.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=cutoff_date, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
