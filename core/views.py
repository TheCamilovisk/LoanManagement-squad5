from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Sum
from decimal import Decimal
from core.serializers import (
    ClientSerializer,
    LoanCreateSerializer,
    LoanSerializer,
    PaymentSerializer,
    PaymentCreateSerializer
)
from core.models import Client, Loan, Payment

def index(request):
    return render(request, 'index.html')

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.api.serializers import (
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
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def payments(request, pk, format=None):
    if request.method == 'GET':
        payments = Payment.objects.filter(loan_id=pk).values()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():

            dt = datetime.strptime(request.data['date'], '%Y-%m-%dT%H:%M')
            year = dt.year
            month = dt.month
            payd_month = Payment.objects.filter(created__month=month, created__year=year)
            
            if (payd_month):
                return Response({'error': 'it is not possible to make two payments in the month'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                loan = Loan.objects.get(id=pk)
                
                amount = float(request.data['amount'])
                payment = request.data['payment']
                
                loan_total = round((loan.installment*loan.term), 2)
                loan_paid = Payment.objects.filter(loan_id=pk, payment='made').aggregate(Sum('amount'))['amount__sum'] or 0.00            
                loan_paid = round(loan_paid + amount, 2)
                
                if (loan_paid > loan_total):
                    return Response({'error': 'it is not possible to pay a value above the loan amount'}, 
                        status=status.HTTP_400_BAD_REQUEST)   
                elif (loan_paid == loan_total):
                    serializer.save(user=request.user, loan=loan)
                    loan.paid = True
                    loan.save()                
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    serializer.save(user=request.user, loan=loan)              
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
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