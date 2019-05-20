from datetime import datetime

from django.contrib.auth.models import User
from django.urls import resolve
from rest_framework import status
from rest_framework.test import APITestCase

from core import views
from core.models import Loan, Payment


class BalanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='topsecretpwd')
        self.client.login(username='john', password='topsecretpwd')

        client_data = {
            'name': 'Felicity',
            'surname': 'Jones',
            'email': 'felicity@gmail.com',
            'telephone': '11984345678',
            'cpf': '34598712387',
        }
        self.client.post('/clients/', client_data, format='json')

        new_loan = {
            'client': 1,
            'amount': 1000,
            'term': 12,
            'rate': 0.05
        }
        self.client.post('/loans/', new_loan, format='json')

        # Post payment not implemented yet
        '''
        payment1 = {
            'loan': 1,
            'payment': 'made',
            'amount': 85.6,
            'date': datetime.strptime('10042019', '%d%m%Y')
        }
        response = self.client.post('/loans/1/payment', payment1, format='json')
        '''
        payment1 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='made',
            date=datetime.strptime('10042019', '%d%m%Y'),
            amount=85.6,
        )
        payment1.save()

        payment2 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='made',
            date=datetime.strptime('10052019', '%d%m%Y'),
            amount=85.6,
        )
        payment2.save()

        loan_paid = {
            'client': 1,
            'amount': 1000,
            'term': 12,
            'rate': 0.05,
        }
        self.client.post('/loans/', loan_paid, format='json')

        for month in range(1, 13):
            p = Payment(
                loan=Loan.objects.get(pk=2),
                user=self.user,
                payment='made',
                date=datetime.strptime(f'10{month}2018', '%d%m%Y'),
                amount=85.6,
            )
            p.save()

        loan_with_no_payments = {
            'client': 1,
            'amount': 1000,
            'term': 12,
            'rate': 0.05,
        }
        self.client.post('/loans/', loan_with_no_payments, format='json')

        self.response_with_payments = self.client.get('/loans/1/balance/')
        self.response_loan_paid = self.client.get('/loans/2/balance/')
        self.response_no_payments = self.client.get('/loans/3/balance/')
        self.response_loan_not_found = self.client.get('/loans/0/balance/')
        self.response_invalid_id = self.client.get('/loans/a/balance/')

    def test_url_resolves_balance_view(self):
        """URL /loans/1/balance/ must use view balance"""
        view = resolve('/loans/1/balance/')
        self.assertEquals(view.func, views.balance)

    def test_payment(self):
        response = self.client.get('/loans/1/payments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_balance_loan_with_two_payments(self):
        """GET /loans/1/balance/ must return status code 200"""
        self.assertEqual(self.response_with_payments.status_code, status.HTTP_200_OK)

    def test_balance_value(self):
        """GET /loans/1/balance/ must contains 856.00"""
        self.assertContains(self.response_with_payments, 856.00)

    def test_balance_loan_paid_status_code(self):
        """GET /loans/2/balance/ must return status code 200"""
        self.assertEqual(self.response_loan_paid.status_code, status.HTTP_200_OK)

    def test_balance_loan_paid_value(self):
        """GET /loans/2/balance/ must contains 0.00"""
        self.assertContains(self.response_loan_paid, 0.00)

    def test_balance_loan_with_no_payments_value(self):
        """GET /loans/3/balance/ must contains 1027.20"""
        self.assertContains(self.response_no_payments, 1027.32)

    def test_balance_loan_not_found_status_code(self):
        """GET /loans/0/balance/ must return status code 200"""
        self.assertEqual(self.response_loan_not_found.status_code, status.HTTP_200_OK)

    def test_balance_loan_not_found_content(self):
        """GET /loans/0/balance/ must contains Loan not found"""
        self.assertContains(self.response_loan_not_found, 'Loan not found')

    def test_invalid_id(self):
        """GET /loans/a/balance must return status code 404"""
        self.assertEqual(self.response_invalid_id.status_code, status.HTTP_404_NOT_FOUND)
