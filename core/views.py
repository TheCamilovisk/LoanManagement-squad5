from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.serializers import (
    ClientSerializer,
    LoanCreateSerializer,
    LoanSerializer,
    PaymentSerializer,
)
from core.models import Client, Loan, Payment


@api_view(['GET', 'POST'])
def loans(request, format=None):
    if request.method == 'POST':
        serializer = LoanCreateSerializer(data=request.data)
        if serializer.is_valid():
            amount = float(request.data['amount'])
            term = int(request.data['term'])
            rate = float(request.data['rate'])
            r = rate / term
            installment = (r + r / ((1 + r) ** term - 1)) * amount
            serializer.save(user=request.user, installment=installment)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def clients(request, format=None):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save(user=request.user)
        return Response({'client_id': client.id}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def payments(request, pk, format=None):
    if request.method == 'GET':
        payments = Payment.objects.filter(loan_id=pk)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass  # TODO


@api_view(['GET'])
def balance(request, pk, format=None):
    if request.method == 'GET':
        try:
            loan = Loan.objects.get(pk=pk)
            payments_made = Payment.objects.filter(loan=pk).filter(payment='made')
            balance_value = loan.term * loan.installment - len(payments_made) * loan.installment
            context = {'balance': balance_value}
        except:
            context = {'balance': 'Loan not found'}
        return Response(context)
