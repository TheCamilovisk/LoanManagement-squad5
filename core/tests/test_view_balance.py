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

        self.response_loan_not_found = self.client.post('/loans/0/balance/')
        self.response_with_payments = self.client.post('/loans/1/balance/')
        self.response_no_payments = self.client.post('/loans/2/balance/')
        self.response_loan_paid = self.client.post('/loans/3/balance/')
        self.response_invalid_id = self.client.post('/loans/a/balance/')

    def test_url_resolves_balance_view(self):
        """URL /loans/1/balance/ must use view balance"""
        view = resolve('/loans/1/balance/')
        self.assertEquals(view.func, views.balance)

    def test_balance_post_status_code(self):
        """POST /loans/1/balance/ must return status code 200"""
        self.assertEqual(200, self.response_with_payments.status_code)

    def test_balance_value(self):
        """POST /loans/1/balance/ must contains 856.00"""
        self.assertContains(self.response_with_payments, 856.00)

    def test_balance_loan_not_found_status_code(self):
        """POST /loans/0/balance/ must return status code 200"""
        self.assertEqual(200, self.response_loan_not_found.status_code)

    def test_balance_loan_not_found_content(self):
        """POST /loans/0/balance/ must contains Loan not found"""
        self.assertContains(self.response_loan_not_found, 'Loan not found')

    def test_balance_loan_with_no_payments_value(self):
        """POST /loans/2/balance/ must contains 1027.20"""
        self.assertContains(self.response_no_payments, 1027.20)

    def test_balance_loan_paid_status_code(self):
        """POST /loans/3/balance/ must return status code 200"""
        self.assertEqual(200, self.response_loan_paid.status_code)

    def test_balance_loan_paid_value(self):
        """POST /loans/3/balance/ must contains 0.00"""
        self.assertContains(self.response_loan_paid, 0.00)

    def test_invalid_id(self):
        """POST /loans/a/balance must return status code 404"""
        self.assertEqual(404, self.response_invalid_id.status_code)
