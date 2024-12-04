from django.urls import path
from . import views

urlpatterns = [
    path('user/payment/', views.initiate_payment, name = "initiate-payment" ),
    path('verify-payment/<str:tx_ref>/', views.verify_payment, name='verify-payment'),
]
