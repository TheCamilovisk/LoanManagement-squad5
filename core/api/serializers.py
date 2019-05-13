from rest_framework import serializers
from core.models import Client, Loan, Payment


class ClientSerializer(serializers.Serializer):
    class Meta:
        model = Client
        fields = (
            'user',
            'name',
            'surname',
            'email',
            'telephone',
            'cpf'
        )


class LoanSerializer(serializers.Serializer):
    class Meta:
        model = Loan
        fields = (
            'user',
            'client',
            'amount',
            'term',
            'rate',
            'date',
            'installment'
        )


class PaymentSerializer(serializers.Serializer):
    class Meta:
        model = Payment
        fields = (
            'loan',
            'user',
            'payment',
            'date',
            'amount'
        )
