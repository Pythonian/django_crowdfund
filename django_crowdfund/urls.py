from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from crowdfund.views import home, reward, payment_process, payment_done, payment_canceled #, paystack_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:id>/', reward, name='reward'),
    path('payment/', payment_process, name='payment_process'),
    path('done/', payment_done, name='payment_done'),
    path('canceled/', payment_canceled, name='payment_canceled'),
    path('paypal/', include('paypal.standard.ipn.urls')), # new
    path('', home, name='home'),

    # path('pay-with-paystack', include(('paystack.urls', 'paystack'), namespace='paystack')),
    # path('paystack_info/', paystack_info, name='paystack_info'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
