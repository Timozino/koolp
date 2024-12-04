# from django.shortcuts import render
# from django.http import HttpRequest, HttpResponse
# from .forms import PaymentForm


# def initiate_payment(request: HttpRequest) -> HttpResponse:
#     context = {}
    
#     if request.method == "POST":
#         payment_form = PaymentForm(request.POST)
#         if payment_form.is_valid():
#             payment = payment_form.save()
#             context['payment'] = payment
#             # Redirect or render a new template for payment processing
#             return render(request, 'make_payment.html', context)
#         else:
#             # Add the invalid form back to the context to show errors
#             context['payment_form'] = payment_form
#     else:
#         payment_form = PaymentForm()
#         context['payment_form'] = payment_form  # Add the form to the context

#     return render(request, 'initiate_payment.html', context)


from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import CurrencyChoices, PaystackPayment

def initiate_payment(request: HttpRequest) -> HttpResponse:
    context = {}
    
    # Fetch available currencies from the CurrencyChoices model
    currencies = CurrencyChoices.choices

    if request.method == "POST":
        # Capture form data directly from POST request
        customer_name = request.POST.get("customer_name")
        customer_phone = request.POST.get("customer_phone")
        amount = request.POST.get("amount")
        currency = request.POST.get("currency")
        email = request.POST.get("email")

        # Validate fields
        if customer_name and customer_phone and amount and currency and email:
            # Save the payment to the database
            payment = PaystackPayment.objects.create(
                customer_name=customer_name,
                customer_phone=customer_phone,
                amount=amount,
                currency=currency,
                email=email
            )
            context['payment'] = payment
            # Redirect or render a new template for payment processing
            return render(request, 'initiate_payment.html', context)
        else:
            # Add an error message if fields are missing or invalid
            context['error'] = "All fields are required."
    else:
        # If GET request, pass the available currencies to the template
        context['currencies'] = currencies

    return render(request, 'initiate_payment.html', context)

