from django.db import models
from django.conf import settings

class Car(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=15)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.license_plate} - {self.model}"

class Ride(models.Model):
    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_rides')
    pickup_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Ride from {self.pickup_location} to {self.destination} - Status: {self.status}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]
    ride = models.OneToOneField(Ride, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
