from django.conf import settings
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField


class Reward(models.Model):
	name = models.CharField(max_length=255)
	slug = models.SlugField(max_length=50, blank=True)
	amount = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('reward', args=[self.slug])


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
	# phone_number = models.IntegerField('Phone Number (Optional)', 
	# blank=True, null=True)
	reward = models.ForeignKey(Reward, on_delete=models.CASCADE)
	note = models.TextField(blank=True)
	email = models.EmailField(verbose_name='Email')
	created = models.DateTimeField(auto_now_add=True)
	paid = models.BooleanField(default=False)
	braintree_id = models.CharField(max_length=150, blank=True)
	paystack_id = models.CharField(max_length=150, blank=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'Order {self.id}'

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


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, max_length=255)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to='images')
    image_thumbnail = ImageSpecField(source='image',
        processors=[ResizeToFill(700, 150)],
        format='JPEG', options={'quality': 60})
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', args=[str(self.slug)])