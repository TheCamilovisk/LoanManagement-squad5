from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal

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
    elif request.method == 'GET':
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


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
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
