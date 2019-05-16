from rest_framework.serializers import ModelSerializer
from core.models import Client, Loan, Payment


class ClientSerializer(ModelSerializer):
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


class LoanSerializer(ModelSerializer):
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
    
    def create(self, validated_data):
        return Loan.objects.create(**validated_data)


class LoanCreateSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            'client',
            'amount',
            'term',
            'rate',
            'date',
        )


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'loan',
            'user',
            'payment',
            'date',
            'amount'
        )
