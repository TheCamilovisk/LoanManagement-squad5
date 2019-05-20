from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
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


@api_view(['GET', 'POST'])
def loans(request, format=None):
    if request.method == 'POST':
        if is_last_loan_paid(request.data['client']):
            client_status = calc_number_of_missed_payments(request.data['client'])
            if client_status == 'first_loan':
                serializer = LoanCreateSerializer(data=request.data)
                if serializer.is_valid():
                    return calc_installment(serializer, request)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                        )
            elif client_status == 'good_payer':
                new_rate = str(Decimal(request.data['rate']) - Decimal(0.02))
                new_data = {
                    'amount': request.data['amount'],
                    'term': request.data['term'],
                    'client': request.data['client'],
                    'rate': new_rate
                }
                serializer = LoanCreateSerializer(data=new_data)
                if serializer.is_valid():
                    return calc_installment(serializer, request)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            elif client_status == 'bad_payer':
                new_rate = str(Decimal(request.data['rate']) + Decimal(0.04))
                new_data = {
                    'amount': request.data['amount'],
                    'term': request.data['term'],
                    'client': request.data['client'],
                    'rate': new_rate
                }
                serializer = LoanCreateSerializer(data=new_data)
                if serializer.is_valid():
                    return calc_installment(serializer, request)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            elif client_status == 'horrible_payer':
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'error': 'The most recent loan is not fully paid.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


def is_last_loan_paid(client_id):
    try:
        last_loan = Loan.objects.filter(client=client_id).order_by('-id')[0]
        return last_loan.paid
    except IndexError:
        return True

def calc_number_of_missed_payments(client_id):
    try:
        last_loan = Loan.objects.filter(client=client_id).order_by('-id')[0]
        last_loan_payments = Payment.objects.filter(
            loan=last_loan.id, payment='missed'
            )
        number_of_missed_payments = len(last_loan_payments)
        if number_of_missed_payments == 0:
            return 'good_payer'
        elif number_of_missed_payments <= 3:
            return 'bad_payer'
        else:
            return 'deny_loan'
    except IndexError:
        return 'first_loan'


def calc_installment(serializer, request):
    amount = float(request.data['amount'])
    term = int(request.data['term'])
    rate = float(request.data['rate'])
    r = rate / term
    installment = (r + r / ((1 + r) ** term - 1)) * amount
    serializer.save(user=request.user, installment=installment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


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
                installment = round(loan.installment, 2)
                term = round(loan.term, 2)
                
                amount = float(request.data['amount'])
                payment = request.data['payment']
                
                loan_total = round((installment*term), 2)
                loan_paid = Payment.objects.filter(loan_id=pk, payment='made').aggregate(Sum('amount'))['amount__sum'] or 0.00            
                loan_paid = round(loan_paid + amount, 2)

                if (installment == amount):                
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
                else:
                    return Response({'error:', 'value of payment is incorrect'})
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        payments = Payment.objects.filter(loan_id=pk)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def balance(request, pk, format=None):
    if request.method == 'GET':
        try:
            loan = Loan.objects.get(pk=pk)
            serializer = LoanSerializer(loan, many=False)
            installment = float(serializer.data['installment'])
            payments_made = Payment.objects.filter(loan=pk).filter(payment='made')
            balance_value = loan.term * installment - len(payments_made) * installment
        except:
            balance_value = 'Loan not found'
        return Response({'balance': balance_value})
