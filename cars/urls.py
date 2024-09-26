from django.urls import path
from .views import request_ride, view_requests, respond_to_request, create_payment, execute_payment, save_ride_data, support

urlpatterns = [
    path('request/', request_ride, name='request_ride'),
    path('requests/', view_requests, name='view_requests'),
    path('save_ride_data/', save_ride_data, name='save_ride_data'),
    path('support/', support, name='support'),
    path('respond/<int:ride_id>/', respond_to_request, name='respond_to_request'),
    path('payment/create/<int:ride_id>/',
         create_payment, name='create_payment'),
    path('payment/execute/', execute_payment, name='execute_payment'),
]
