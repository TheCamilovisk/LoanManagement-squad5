from rest_framework.viewsets import ModelViewSet
from core.api.serializers import ClientSerializer, LoanSerializer, PaymentSerializer
from core.models import Client, Loan, Payment
from rest_framework.decorators import action


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
