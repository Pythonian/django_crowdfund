from django.conf import settings
from django.urls import reverse
from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill


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
	note = models.TextField(blank=True)
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


class FrequentlyAskedQuestion(models.Model):
	title = models.CharField(max_length=150)

	def __str__(self):
		return self.title


class FrequentlyAskedQuestionDescription(models.Model):
	faq = models.ForeignKey(FrequentlyAskedQuestion, on_delete=models.CASCADE, related_name='faqs')
	description = models.TextField()


class Gallery(models.Model):
	title = models.CharField(max_length=20, blank=True)
	caption = models.CharField(max_length=100, blank=True)
	image = models.ImageField(upload_to='images')
	image_thumbnail = ImageSpecField(source='image',
		processors=[ResizeToFill(380, 254)],
		format='JPEG', options={'quality': 60})

	class Meta:
		verbose_name_plural = 'Galleries'

	def __str__(self):
		return self.caption


class Section(models.Model):
	title = models.CharField(max_length=50)
	content = models.TextField()
	image = models.ImageField(upload_to='images', blank=True)

	def __str__(self):
		return self.title	

	
# class PaystackInfo(models.Model):
# 	full_name = models.CharField(max_length=150)
# 	email = models.EmailField()
# 	phone_number = models.CharField(max_length=20)
# 	amount = models.IntegerField()
# 	address = models.CharField(max_length=150)

# 	def __str__(self):
# 		return self.full_name