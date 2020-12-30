from celery import shared_task
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Order


@shared_task
def payment_successful_email(order_id):
    order = get_object_or_404(Order, id=order_id)
    mail_sent = send_mail(
        subject='Thank you for your contribution on When Will I Be Famous?',
        message=render_to_string('acknowledgment.txt', {'order': order}),
        from_email=settings.AUTHOR_EMAIL,
        recipient_list=[order.email],
        fail_silently=False,
        html_message=render_to_string('acknowledgment.html', {'order': order}))
    return mail_sent
