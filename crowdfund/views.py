# import braintree
import datetime
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from .models import Reward, Order, FrequentlyAskedQuestion, Section, Gallery
from .forms import OrderCreateForm


# instantiate Braintree payment gateway
# gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def intWithCommas(x):
	if x < 0:
		return '-' + intWithCommas(-x)
	result = ''
	while x >= 1000:
		x, r = divmod(x, 1000)
		result = ",%03d%s" % (r, result)
	return "%d%s" % (x, result)


def get_context():
	total = Order.objects.filter(paid=True).aggregate(Sum('reward__amount'))['reward__amount__sum']
	pct = ((100 * float(total) / float(settings.GOAL)) if total else 0)
	c = {
		'goal': intWithCommas(settings.GOAL),
		'faqs': FrequentlyAskedQuestion.objects.all(),
		'backers': Order.objects.filter(paid=True).count(),
		'pct': pct,
		'pct_disp': (int(pct) if total else 0),
		'total': (intWithCommas(int(total)) if total else '0'),
		'rewards': sorted(Reward.objects.all(), key=lambda i: i.amount),
		'sections': Section.objects.all(),
		'photos': Gallery.objects.all()
		}
	return c


def home(request):
	return render(request, 'home.html', get_context())


def reward(request, id):
	reward = get_object_or_404(Reward, id=id)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save(commit=False)
			order.reward = reward
			order.save()
			request.session['order_id'] = order.id
			# redirect for payment
			return redirect(reverse('payment_process'))
	else:
		form = OrderCreateForm()
	return render(request,
				  'reward.html',
				  {'form': form, 'reward': reward})

# Using Braintree

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

# Using Paystack

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
    return render(request, 'process_paypal.html', {'order': order, 'paypal_form': paypal_form, 'paystack_key': settings.PAYSTACK_PUBLIC_KEY})

@csrf_exempt
def payment_done(request):
    return render(request, 'done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'canceled.html')


# from .forms import PaystackInfoForm

# def paystack_info(request):
# 	if request.method == 'POST':
# 		paystack_form = PaystackInfoForm(request.POST)
# 		if paystack_form.is_valid():
# 			paystack_form.save()
# 			return render(request, 'paystack.html',
# 				{'email': paystack_form.email, 'phone_number': paystack_form.phone_number, 'amount': paystack_form.amount})
# 		else:
# 			return render(request, 'canceled.html')
# 	else:
# 		paystack_form = PaystackInfoForm()
# 	return render(request, 'paystack_info.html', {'paystack_form': paystack_form})