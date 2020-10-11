import braintree
import datetime
from django.db.models import Sum
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Reward, Order
from .forms import OrderCreateForm


# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


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
		'backers': Order.objects.filter(paid=True).count(),
		'pct': pct,
		'pct_disp': (int(pct) if total else 0),
		'total': (intWithCommas(int(total)) if total else '0'),
		# 'nopay': (True if settings.STOP and (settings.DATE - datetime.datetime.now()).days < 0 else False),
		# 'days': (settings.DATE - datetime.datetime.now()).days,
		'rewards': sorted(Reward.objects.all(), key=lambda i: i.amount),
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


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_cost()

    if request.method == 'POST':
        # retrieve nonce to generate a new transaction
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                # transaction automatically submitted for settlement.
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment_done')
        else:
            return redirect('payment_canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(request,
                      'payment.html',
                      {'order': order,
                       'client_token': client_token})


def payment_done(request):
    return render(request, 'done.html')


def payment_canceled(request):
    return render(request, 'canceled.html')
