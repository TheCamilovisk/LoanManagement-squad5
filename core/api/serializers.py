from rest_framework.serializers import ModelSerializer
from core.models import Client, Loan, Payment


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'user',
            'name',
            'surname',
            'email',
            'telephone',
            'cpf'
        )


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            'id',
            'user',
            'client',
            'amount',
            'term',
            'rate',
            'date',
            'installment'
        )


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'id',
            'loan',
            'user',
            'payment',
            'date',
            'amount'
        )
