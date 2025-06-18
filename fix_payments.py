# from api.core.models import PaymentHistory
# import datetime
# from django.utils.timezone import make_aware

# # Identify problematic rows
# for ph in PaymentHistory.objects.all():
#     if isinstance(ph.date, datetime.date) and not isinstance(ph.date, datetime.datetime):
#         # Convert to datetime (e.g., midnight of that day)
#         fixed_date = make_aware(datetime.datetime.combine(ph.date, datetime.time.min))
#         ph.date = fixed_date
#         ph.save()
