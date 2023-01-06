from django.urls import path
from . import views

urlpatterns = [
    path('deposit/<int:pk>/', views.deposit, name='deposit'),
    path('withdraw/<int:pk>/', views.withdraw, name='withdraw'),
    path('transfer/<int:pk>/', views.transfer, name='transfer'),
    path('payment/<int:pk>/', views.payment, name='payment'),
    path('schedule_payment/<int:pk>/', views.schedule_payment, name='schedule_payment'),
    path('cancel_scheduled_payment/<int:pk>/', views.cancel_scheduled_payment, name='cancel_scheduled_payment'),
    
    # Third party payments
    path('third_party/paypal/', views.paypal_auth, name='paypal'),
    path("make_payment/", views.make_payment, name="make_payment"),
    path("refund_payment/<int:payment_id>/", views.refund_payment, name="refund_payment"),
]
