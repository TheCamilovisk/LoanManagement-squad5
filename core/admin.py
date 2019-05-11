from django.contrib import admin
from core.models import Client, Loan, Payment

admin.site.register(Client)
admin.site.register(Loan)
admin.site.register(Payment)