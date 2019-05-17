from datetime import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.api.serializers import LoanSerializer, ClientSerializer, PaymentSerializer, LoanCreateSerializer
from core.models import Client, Loan, Payment

@api_view(['GET', 'POST'])
def loans(request, format=None):
    if request.method == 'POST':
        serializer = LoanCreateSerializer(data=request.data)
        #4
        if serializer.is_valid():
            amount = float(request.data['amount'])
            term = int(request.data['term'])
            rate = float(request.data['rate'])
            r = rate/term
            installment = (r + r / ((1 + r) ** term - 1)) * amount
            serializer.save(user=request.user, installment=installment)
            #headers = self.get_sucess_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            #    headers=headers
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
def payments(request, pk=None):

    if request.method == 'GET':
        '''
        data = {
            'loan_id' : pk,
            'payment': 'made',
            'date' : '2019-05-16T11:24:08z',
            'amount': '85.60'
        }
        return Response(data)
        '''
        payments = Payment.objects.filter(loan_id=pk).values()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        '''
        data = {
            'loan_id' : pk,
            'payment' : request.data.get('payment'),
            'date' : request.data.get('date'),
            'amount' : request.data.get('amount')
        }
        return Response(data, status=status.HTTP_201_CREATED)
        '''
        validator = validator_payment(request, pk)
        if len(validator) == 0:
            data = {
                'loan_id' : pk,
                'payment' : request.data.get('payment'),
                'date' : request.data.get('date'),
                'amount' : request.data.get('amount')
            }
            loan = Loan.objects.get(id=pk)
            serializer = PaymentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(loan=loan)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(validator, status=status.HTTP_400_BAD_REQUEST)

def validator_payment(request, pk):
    
    payment = request.data.get('payment')
    date = request.data.get('date')
    amount = request.data.get('amount')

    msg = []

    if (len(payment) > 6):
        msg.append({'msg':'check if the type of payment is correct'})

    if payment not in ('made', 'missed'):
        msg.append({'msg':'type of payment should by "made" or "missed"'})
    
    try:
        datetime.strptime(date, '%Y-%m-%dT%H:%Mz')
    except ValueError:
        msg.append({'msg':'date should by in format ISO 8601 "%Y-%m-%dT%H:%Mz"'})

    try:
        date = datetime.strptime(date, '%Y-%m-%dT%H:%Mz').date()
        current = datetime.now().date()
        if (date != current):
            msg.append({'msg':'the date can not be different from the current date'})
    except ValueError:
        msg.append({'msg':'the date can not be different from the current date'})

    try:
        float(amount)
    except:
       msg.append({'msg':'the amount should by valid. i.e: 1000'}) 

    return msg


@api_view(['POST'])
def balance(request, pk, format=None):
    if request.method == 'POST':
        pass #TODO