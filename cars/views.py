import json
from .models import Ride, Payment
from django.http import JsonResponse
from django.conf import settings
import paypalrestsdk
from django.shortcuts import render, redirect
# from .forms import RideRequestForm
from .models import Ride
from django.contrib.auth.decorators import login_required


@login_required
def request_ride(request):
    return render(request, 'cars/request_ride.html')


@login_required
def save_ride_data(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)
        pickup_location = data.get('pickup')
        destination = data.get('destination')

        # Create and save the RideRequest object
        if pickup_location and destination:
            ride = Ride.objects.create(
                rider=request.user,
                pickup_location=pickup_location,
                destination=destination,
            )
            ride.save()

            # Return a success message as JSON
            return JsonResponse({'status': 'success', 'message': 'Ride data saved successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid ride data.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def view_requests(request):
    if request.user.is_driver:
        rides = Ride.objects.filter(status='Pending').values('id',
                                                             'pickup_location', 'destination')
        return render(request, 'cars/view_requests.html', {'rides': list(rides)})
    else:
        return redirect('home')


@login_required
def respond_to_request(request, ride_id):
    if request.user.is_driver:
        ride = Ride.objects.get(id=ride_id)
        if request.method == 'POST':
            ride.driver = request.user
            ride.status = 'Accepted'
            ride.save()
            return redirect('view_requests')
        return render(request, 'cars/respond_to_request.html', {'ride': ride})
    else:
        return redirect('home')


def support(request):
    return render(request, 'pages/support.html')


paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


def create_payment(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    amount = 20  # Implement this function to calculate the cost

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri('/payment/execute/'),
            "cancel_url": request.build_absolute_uri('/payment/cancel/')
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Taxi Ride",
                    "sku": "item",
                    "price": str(amount),
                    "currency": "AUD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(amount),
                "currency": "AUD"
            },
            "description": "Payment for taxi ride"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return JsonResponse({'error': 'Payment creation failed'}, status=500)


def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        # Update payment status in your database
        return redirect('home')
    else:
        return JsonResponse({'error': 'Payment execution failed'}, status=500)
