from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from core.models import Client, Loan, Payment

from .validators import validate_cpf


class ClientSerializer(ModelSerializer):
    cpf = serializers.CharField(validators=[validate_cpf])

    class Meta:
        model = Client
        fields = ('name', 'surname', 'email', 'telephone', 'cpf')


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = ('user', 'client', 'amount', 'term', 'rate', 'date', 'installment')

    def create(self, validated_data):
        return Loan.objects.create(**validated_data)


class LoanCreateSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = ('client', 'amount', 'term', 'rate', 'date')


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('loan', 'user', 'payment', 'date', 'amount')
