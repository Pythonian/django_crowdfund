from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from paypal.standard.ipn.signals import valid_ipn_received
from paystack.api.signals import payment_verified

from .models import Order
from .tasks import payment_successful_email


@receiver(payment_verified)
def on_payment_verified(sender, ref, amount, order, **kwargs):
    """
    ref: paystack reference sent back.
    amount: amount in Naira.
    order: paystack id tied to the user.
    """
    get_order = get_object_or_404(Order, paystack_id=order)
    get_order.paid = True
    get_order.save()
    payment_successful_email.delay(get_order.id)


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == 'Completed':
        order = get_object_or_404(Order, id=ipn.invoice)

        if order.get_cost() == ipn.mc_gross:
            order.paid = True
            order.save()
            payment_successful_email.delay(order.id)
