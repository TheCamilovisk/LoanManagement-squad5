from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.api.serializers import LoanSerializer, ClientSerializer, PaymentSerializer
from core.utils import calc_installment
from core.models import Client, Loan, Payment

@api_view(['GET', 'POST'])
def loans(request, format=None):
    if request.method == 'POST':
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            amount = float(request.data['amount'])
            term = int(request.data['term'])
            rate = float(request.data['rate'])
            r = rate/term
            installment = (r + r / ((1 + r) ** term - 1)) * amount
            serializer.save(user=request.user, installment=installment)
            headers = self.get_sucess_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
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
        pass #TODO


@api_view(['GET', 'POST'])
def payments(request, pk, format=None):
    if request.method == 'GET':
        payments = Payment.objects.filter(loan_id=pk)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        pass #TODO


@api_view(['POST'])
def balance(request, pk, format=None):
    if request.method == 'POST':
        pass #TODO