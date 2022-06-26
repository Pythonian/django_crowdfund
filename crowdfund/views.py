# import braintree
from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm

from .forms import ContactForm, OrderCreateForm
from .models import (FrequentlyAskedQuestion, Gallery,
                     Order, Reward, Section, Post)


def intWithCommas(x):
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


def home(request):
    total = Order.objects.filter(paid=True).aggregate(
        Sum('reward__amount'))['reward__amount__sum']
    pct = ((100 * float(total) / float(settings.GOAL)) if total else 0)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email,
                          ['authorphilips@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('home')
    form = ContactForm()
    context = {
        'goal': settings.GOAL,
        'faqs': FrequentlyAskedQuestion.objects.all(),
        'backers': Order.objects.filter(paid=True).count(),
        'pct': pct,
        'pct_disp': (int(pct) if total else 0),
        'total': (intWithCommas(int(total)) if total else '0'),
        'rewards': sorted(Reward.objects.all(), key=lambda i: i.amount),
        'sections': Section.objects.all(),
        'photos': Gallery.objects.all(),
        'form': form,
    }
    return render(request, 'home.html', context)


def reward(request, slug):
    reward = get_object_or_404(Reward, slug=slug)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.reward = reward
            order.save()
            request.session['order_id'] = order.id
            return redirect(reverse('payment_process'))
    else:
        form = OrderCreateForm()
    return render(request,
                  'reward.html',
                  {'form': form, 'reward': reward})


# Instantiate Braintree payment gateway
# gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

# def payment_process(request):
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#     total_cost = order.get_cost()

#     if request.method == 'POST':
#         # retrieve nonce to generate a new transaction
#         nonce = request.POST.get('payment_method_nonce', None)
#         # create and submit transaction
#         result = gateway.transaction.sale({
#             'amount': f'{total_cost:.2f}',
#             'payment_method_nonce': nonce,
#             'options': {
#                 # transaction automatically submitted for settlement.
#                 'submit_for_settlement': True
#             }
#         })
#         if result.is_success:
#             # mark the order as paid
#             order.paid = True
#             # store the unique transaction id
#             order.braintree_id = result.transaction.id
#             order.save()
#             return redirect('payment_done')
#         else:
#             return redirect('payment_canceled')
#     else:
#         # generate token
#         client_token = gateway.client_token.generate()
#         return render(request,
#                       'payment.html',
#                       {'order': order,
#                        'client_token': client_token})


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_cost().quantize(
            Decimal('.01')),
        'item_name': 'Order {}'.format(order.reward.name),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'https://{}{}'.format(host,
                                            reverse('paypal-ipn')),
        'return_url': 'https://{}{}'.format(host,
                                            reverse('payment_done')),
        'cancel_return': 'https://{}{}'.format(host,
                                               reverse('payment_canceled')),
    }
    paypal_form = PayPalPaymentsForm(initial=paypal_dict, button_type="donate")

    paystack_amount = int(order.get_cost() * 476 * 100)
    paystack_ref = None
    if not paystack_ref:
        paystack_ref = get_random_string().upper()
        order.paystack_id = paystack_ref
        order.save()
    paystack_redirect_url = "{}?amount={}".format(
        reverse('paystack:verify_payment',
                args=[paystack_ref]), paystack_amount)

    return render(request, 'process_payment.html',
                  {'order': order, 'paypal_form': paypal_form,
                   'paystack_key': settings.PAYSTACK_PUBLIC_KEY,
                   'paystack_amount': paystack_amount,
                   'paystack_redirect_url': paystack_redirect_url})


@csrf_exempt
def payment_done(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'done.html', {'order': order})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'canceled.html')


def post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    return render(request, 'post.html', {'post': post})


def contact_success(request):
    return HttpResponse('Success! Thank you for your message.')
