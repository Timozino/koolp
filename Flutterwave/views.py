from django.shortcuts import render






from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from .forms import PaymentForm
from .models import Payment
from .wavePayment import FlutterWave

def initiate_payment(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()  # Save the payment data
            flutterwave = FlutterWave()
            return redirect(flutterwave.create_checkout_url(payment))
        else:
            context['message'] = "Payment failed. Please correct the errors below."
    else:
        form = PaymentForm()

    context['form'] = form
    return render(request, 'initiate_payment.html', context)





def verify_payment(request: HttpRequest, tx_ref: str) -> HttpResponse:
    print(f"Received request for tx_ref: {tx_ref}")
    try:
        payment = get_object_or_404(Payment, tx_ref=tx_ref)
        print(f"Found payment: {payment}")

        transaction_id = request.GET.get('transaction_id')
        print(f"Transaction ID from request: {transaction_id}")

        flutterwave = FlutterWave()
        verified, data = flutterwave.verify_payment(tx_ref, transaction_id)

        if verified:
            payment.verified = True
            payment.status = "success"
            payment.save()
            print(f"Payment verification succeeded for tx_ref: {tx_ref}")
            messages.success(request, "Payment verified successfully.")
        else:
            print(f"Payment verification failed: {data}")
            messages.error(request, f"Payment verification failed: {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"Error in verify_payment view: {e}")
        messages.error(request, "An error occurred during payment verification.")

    return redirect('initiate-payment')
