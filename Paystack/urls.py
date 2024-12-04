from django.urls import path
from . import views

urlpatterns =[
    path('user/payments/', views.initiate_payment, name = "initiate-payment"),
]