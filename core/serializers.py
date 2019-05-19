from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from core.models import Client, Loan, Payment

from .validators import validate_cpf, validate_telephone


class ClientSerializer(ModelSerializer):
    cpf = serializers.CharField(
        validators=[UniqueValidator(queryset=Client.objects.all()), validate_cpf]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Client.objects.all()), EmailValidator()]
    )
    telephone = serializers.CharField(validators=[validate_telephone])

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
        fields = ('id', 'loan_id', 'user_id', 'payment', 'date', 'amount')

class PaymentCreateSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('payment', 'date', 'amount')

