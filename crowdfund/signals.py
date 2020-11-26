from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from paystack.api.signals import payment_verified
from .models import Order


@receiver(payment_verified)
def on_payment_verified(sender, ref, amount, order, **kwargs):
    """
    ref: paystack reference sent back.
    amount: amount in Naira.
    """
    get_order = get_object_or_404(Order, braintree_id=order)
    get_order.paid = True
    get_order.save()


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        # payment was successful
        order = get_object_or_404(Order, id=ipn.invoice)

        if order.get_cost() == ipn.mc_gross:
            # mark the order as paid
            order.paid = True
            order.save()
    #     send_mail(
				# subject='Thank you for your contribution on When Will I Be Famous?',
				# message=get_template('acknowledgment.txt').render(Context(
				# 	{'order': order})),
				# from_email=settings.AUTHOR_EMAIL,
				# recipient_list=[order.email],
				# fail_silently=False)