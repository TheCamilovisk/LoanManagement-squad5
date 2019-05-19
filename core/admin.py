from django.contrib import admin
from core.models import Client, Loan, Payment

class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'surname', 'email', 'telephone', 'cpf', 'created', 'updated')
    list_display_links = ('id', 'name')


class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'client', 'amount', 'term', 'rate', 'date', 'installment', 'created', 'updated')
    list_display_links = ('id', 'client')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'loan', 'payment', 'date', 'created', 'updated')
    list_display_links = ('id', 'loan')   


admin.site.register(Client, ClientAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Payment, PaymentAdmin)