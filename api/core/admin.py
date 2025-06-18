# core/admin.py

from django.contrib import admin
from .models import ClientProfile, PaymentHistory, VolunteerProfile, Task

class PaymentHistoryInline(admin.TabularInline):
    model = PaymentHistory
    extra = 0

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'party_name', 'total_amount', 'amount_paid', 'due_amount', 'joined_date')
    search_fields = ('user__name', 'user__email', 'party_name')
    inlines = [PaymentHistoryInline]

    def amount_paid(self, obj):
        return obj.amount_paid
    amount_paid.short_description = 'Amount Paid'

    def due_amount(self, obj):
        return obj.due_amount
    due_amount.short_description = 'Due Amount'

@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'joined_date')
    search_fields = ('user__name', 'user__email', 'skills')


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'amount_paid')
    list_filter = ('date', 'client')
    search_fields = ('client__user__name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'assigned_to', 'status', 'created_on')
    list_filter = ('status', 'client', 'assigned_to')
    search_fields = ('name', 'description')

