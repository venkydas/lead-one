# core/models.py

from django.db import models
from api.users.models import User
import datetime
from django.utils.timezone import make_aware

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'CLIENT'})
    party_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    joined_date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.name} - {self.party_name}"

    @property
    def amount_paid(self):
        # Sum of all payments
        return sum(payment.amount_paid for payment in self.paymenthistory_set.all())

    @property
    def due_amount(self):
        return self.total_amount - self.amount_paid

class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'VOLUNTEER'})
    skills = models.TextField()
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class PaymentHistory(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Ensure `date` is always a datetime.datetime (not just date)
        if isinstance(self.date, datetime.date) and not isinstance(self.date, datetime.datetime):
            self.date = make_aware(datetime.datetime.combine(self.date, datetime.time.min))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.amount_paid} on {self.date} for {self.client.user.name}"

class Task(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return self.name
