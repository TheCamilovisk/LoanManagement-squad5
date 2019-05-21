from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from decimal import Decimal
from datetime import datetime
from core.serializers import (
    ClientSerializer,
    LoanCreateSerializer,
    LoanSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
)
from core.models import Client, Loan, Payment


@api_view(["GET", "POST"])
def loans(request, format=None):
    if request.method == "POST":
        client_id = request.data["client"]
        if is_last_loan_paid(client_id):
            client_status = calc_number_of_missed_payments(request.data["client"])
            if client_status == "first_loan":
                serializer = LoanCreateSerializer(data=request.data)
                if serializer.is_valid():
                    return calc_installment(serializer, request)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            elif client_status == "good_payer":
                new_rate = str(Decimal(request.data["rate"]) - Decimal(0.02))
                new_data = {
                    "amount": request.data["amount"],
                    "term": request.data["term"],
                    "client": request.data["client"],
                    "rate": new_rate,
                }
                serializer = LoanCreateSerializer(data=new_data)
                if serializer.is_valid():
                    return calc_installment(serializer, request)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            elif client_status == "bad_payer":
                new_rate = str(Decimal(request.data["rate"]) + Decimal(0.04))
                new_data = {
                    "amount": request.data["amount"],
                    "term": request.data["term"],
                    "client": request.data["client"],
                    "rate": new_rate,
                }
                serializer = LoanCreateSerializer(data=new_data)
                if serializer.is_valid():
                    return calc_installment(serializer, request)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            elif client_status == "horrible_payer":
                return Response(
                    {"error": "Loan denied due to client's payment history."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "The most recent loan is not fully paid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    elif request.method == "GET":
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


def get_last_loan_id(client_id):
    try:
        last_loan = Loan.objects.filter(client=client_id).order_by("-id")[0]
        return last_loan.id
    except IndexError:
        return 0


def is_last_loan_paid(client_id):
    last_loan_id = get_last_loan_id(client_id)
    if last_loan_id == 0:
        return True
    else:
        loan = Loan.objects.get(pk=last_loan_id)
        serializer = LoanSerializer(loan, many=False)
        installment = float(serializer.data["installment"])
        payments_made = Payment.objects.filter(loan=last_loan_id).filter(payment="made")
        balance_value = round(
            (loan.term * installment - len(payments_made) * installment), 2
        )
        if balance_value == 0:
            return True
        else:
            return False


def calc_number_of_missed_payments(client_id):
    try:
        last_loan = Loan.objects.filter(client=client_id).order_by("-id")[0]
        last_loan_payments = Payment.objects.filter(loan=last_loan.id, payment="missed")
        number_of_missed_payments = len(last_loan_payments)
        if number_of_missed_payments == 0:
            return "good_payer"
        elif number_of_missed_payments <= 3:
            return "bad_payer"
        else:
            return "horrible_payer"
    except IndexError:
        return "first_loan"


def calc_installment(serializer, request):
    amount = float(request.data["amount"])
    term = int(request.data["term"])
    rate = float(request.data["rate"])
    r = rate / term
    installment = (r + r / ((1 + r) ** term - 1)) * amount
    serializer.save(user=request.user, installment=installment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def clients(request, format=None):
    if request.method == "GET":
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save(user=request.user)
        return Response({"client_id": client.id}, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def payments(request, pk, format=None):
    if request.method == "GET":
        payments = Payment.objects.filter(loan_id=pk)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        try:
            loan = loan_exists(pk)
            if loan is False:
                raise Exception({'detail': 'loan not found'})

            serializer = PaymentCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            amount = float(request.data["amount"])
            installment = round(float(loan.installment), 2)
            term = round(float(loan.term), 2)
            loan_total = round((installment * term), 2)
            loan_paid = (
                Payment.objects.filter(loan_id=pk, payment="made").aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0.00
            )
            loan_paid = round(float(loan_paid), 2) + round(float(amount), 2)

            if installment != amount:
                raise Exception({"detail:": "value of payment is incorrect"})

            if loan_paid > loan_total:
                raise Exception(
                    {
                        "detail": "it is not possible to pay a value above the loan amount"
                    }
                )
            elif loan_paid == loan_total:
                serializer.save(user=request.user, loan=loan)
                loan.paid = True
                loan.save()
            else:
                serializer.save(user=request.user, loan=loan)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({str(e)}, status=status.HTTP_400_BAD_REQUEST)


def loan_exists(pk):
    try:
        loan = Loan.objects.get(id=pk)
        return loan
    except Exception as e:
        return False


@api_view(["GET"])
def balance(request, pk, format=None):
    if request.method == "GET":
        try:
            loan = Loan.objects.get(pk=pk)
            serializer = LoanSerializer(loan, many=False)
            installment = float(serializer.data["installment"])
            payments_made = Payment.objects.filter(loan=pk).filter(payment="made")
            balance_value = round(
                (loan.term * installment - len(payments_made) * installment), 2
            )
        except:
            balance_value = "Loan not found"
        return Response({"balance": balance_value})
