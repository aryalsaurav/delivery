from celery import shared_task

from datetime import datetime
from django.core.mail import send_mail

from .models import User


@shared_task
def brithday_wish():
    today = datetime.now()
    users = User.objects.filter(dob__month=today.month,dob__day=today.day)
    for user in users:
        send_mail(
            'Happy Birthday!',
            f'Dear {user.full_name} Happy Birthday',
            'noreply@gmail.com',
            [user.email],
            fail_silently=False
        )
