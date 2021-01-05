from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from crowdfund.views import home, reward, payment_process, payment_done, payment_canceled, post

urlpatterns = [
    path('wwibfadmin/', admin.site.urls),
    #path('ckeditor/', include('ckeditor_uploader.urls')),
    path('payment/', payment_process, name='payment_process'),
    path('done/', payment_done, name='payment_done'),
    path('canceled/', payment_canceled, name='payment_canceled'),
    path('b/<slug:post_slug>/', post, name='post'),
    path('<slug:slug>/', reward, name='reward'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paystack/', include(('paystack.frameworks.django.urls', 'paystack'), namespace='paystack')),
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
