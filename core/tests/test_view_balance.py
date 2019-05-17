from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from core import views
from ..models import Client, Loan, Payment


class BalanceTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        user.save()

        client = Client(
            user=user,
            name='John',
            surname='Lennon',
            email='john@email.com',
            telephone='11234567890',
            cpf='11122233345',
        )
        client.save()

        new_loan = Loan(
            user=user,
            client=client,
            amount=1000,
            term=12,
            rate=0.5,
            date=datetime.strptime('10032019', '%d%m%Y'),
            installment=85.6
        )
        new_loan.save()

        payment1 = Payment(
            loan=new_loan,
            user=user,
            payment='made',
            date=datetime.strptime('10042019', '%d%m%Y'),
            amount=85.6,
        )
        payment1.save()

        payment2 = Payment(
            loan=new_loan,
            user=user,
            payment='made',
            date=datetime.strptime('10052019', '%d%m%Y'),
            amount=85.6,
        )
        payment2.save()

        loan_with_no_payments = Loan(
            user=user,
            client=client,
            amount=1000,
            term=12,
            rate=0.5,
            date=datetime.strptime('10032019', '%d%m%Y'),
            installment=85.6
        )
        loan_with_no_payments.save()

        loan_paid = Loan(
            user=user,
            client=client,
            amount=1000,
            term=12,
            rate=0.5,
            date=datetime.strptime('10032019', '%d%m%Y'),
            installment=85.6
        )
        loan_paid.save()

        for payment in range(12):
            p = Payment(
                loan=loan_paid,
                user=user,
                payment='made',
                date=datetime.strptime('10052019', '%d%m%Y'),
                amount=85.6,
            )
            p.save()

        self.response_invalid = self.client.post('/loans/0/balance/')
        self.response_valid = self.client.post('/loans/1/balance/')
        self.response_no_payments = self.client.post('/loans/2/balance/')
        self.response_loan_paid = self.client.post('/loans/3/balance/')
