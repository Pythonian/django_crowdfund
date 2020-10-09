from django.conf import settings
from django.urls import reverse
from django.db import models


class Reward(models.Model):
	name = models.CharField(max_length=255)
	amount = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('reward', args=[self.id])


class Perk(models.Model):
	description = models.CharField(max_length=255)
	reward = models.ForeignKey(Reward, on_delete=models.CASCADE, related_name='perks')
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.description


class Order(models.Model):
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
	email = models.EmailField(verbose_name='Email')
	created = models.DateTimeField(auto_now_add=True)
	paid = models.BooleanField(default=False)
	braintree_id = models.CharField(max_length=150, blank=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'Order {self.id}'

	# def get_total_cost(self):
	#     total_cost = sum(item.get_cost() for item in self.items.all())
	#     return total_cost - total_cost * \
	#         (self.discount / Decimal(100))

	def __str__(self):
		return self.name

	def get_cost(self):
		return self.reward.amount