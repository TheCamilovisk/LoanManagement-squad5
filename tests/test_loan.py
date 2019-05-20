from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Loan, Payment
from datetime import datetime


class LoanTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='squad5', email='squad5@gmail.com', password='5dauqs'
        )
        client_data = {
            'name': 'Felicity',
            'surname': 'Jones',
            'email': 'felicity@gmail.com',
            'telephone': '11984345678',
            'cpf': '34598712376',
        }
        self.client.login(username='squad5', password='5dauqs')
        self.client.post('/clients/', data=client_data, format='json')

    def test_create_complete_loan(self):
        loan_data1 = {
            'client': 1,
            'amount': 1000,
            'term': 12,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data1, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), 1)

    def test_create_loan_improper_amount(self):
        loan_data2 = {
            'client': 1,
            'amount': -1000.0,
            'term': 12,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        loan_data3 = {
            'client': 1,
            'amount': 0,
            'term': 12,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data3, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'amount', status_code=status.HTTP_400_BAD_REQUEST)

    def test_create_loan_improper_term(self):
        loan_data4 = {
            'client': 1,
            'amount': 1000,
            'term': 0,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data4, format='json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'term', status_code=status.HTTP_400_BAD_REQUEST)
        loan_data5 = {
            'client': 1,
            'amount': 1000,
            'term': -12,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data5, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_loan_improper_rate(self):
        loan_data6 = {
            'client': 1,
            'amount': 1000,
            'term': 12,
            'rate': 0,
        }
        response = self.client.post('/loans/', data=loan_data6, format='json')
        self.assertContains(response, 'rate', status_code=status.HTTP_400_BAD_REQUEST)

        loan_data7 = {
            'client': 1,
            'amount': 1000,
            'term': 12,
            'rate': -0.05,
        }
        response = self.client.post('/loans/', data=loan_data7, format='json')
        self.assertContains(response, 'rate', status_code=status.HTTP_400_BAD_REQUEST)

        loan_data8 = {
            'client': 1,
            'amount': 1000,
            'term': 12,
            'rate': 2,
        }
        response = self.client.post('/loans/', data=loan_data8, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_loan_good_payer(self):
        loan_data9 = {
            'client': 1,
            'amount': 100,
            'term': 2,
            'rate': 0.05,
        }
        self.client.post('/loans/', data=loan_data9, format='json')

        payment1 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='made',
            date=datetime.strptime('10062019', '%d%m%Y'),
            amount=51.88,
        )
        payment1.save()

        payment2 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='made',
            date=datetime.strptime('10072019', '%d%m%Y'),
            amount=51.88,
        )
        payment2.save()

        loan_data10 = {
            'client': 1,
            'amount': 100,
            'term': 2,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data10, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(round(response.data['rate'], 2), 0.03)

    def test_create_loan_bad_payer(self):
        loan_data11 = {
            'client': 1,
            'amount': 100,
            'term': 2,
            'rate': 0.05,
        }
        self.client.post('/loans/', data=loan_data11, format='json')

        payment3 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='missed',
            date=datetime.strptime('18052019', '%d%m%Y'),
            amount=50.31
        )
        payment3.save()

        payment4 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='made',
            date=datetime.strptime('18062019', '%d%m%Y'),
            amount=50.31
        )
        payment4.save()

        payment5 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='missed',
            date=datetime.strptime('18072019', '%d%m%Y'),
            amount=50.31
        )
        payment5.save()

        payment6 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment='made',
            date=datetime.strptime('18082019', '%d%m%Y'),
            amount=50.31
        )
        payment6.save()

        loan_data12 = {
            'client': 1,
            'amount': 100,
            'term': 2,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data12, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(round(response.data['rate'], 2), 0.09)

    def test_create_loan_horrible_payer(self):
        loan_data13 = {
            'client': 1,
            'amount': 300,
            'term': 2,
            'rate': 0.05,
        }
        self.client.post('/loans/', data=loan_data13, format='json')

        payment7 = Payment(
            user=self.user,
            loan=Loan.objects.get(pk=1),
            payment='missed',
            amount=150.94,
            date=datetime.strptime('18052019', '%d%m%Y')
        )
        payment7.save()

        payment8 = Payment(
            user=self.user,
            loan=Loan.objects.get(pk=1),
            payment='missed',
            amount=150.94,
            date=datetime.strptime('18062019', '%d%m%Y')
        )
        payment8.save()

        payment9 = Payment(
            user=self.user,
            loan=Loan.objects.get(pk=1),
            payment='missed',
            amount=150.94,
            date=datetime.strptime('18072019', '%d%m%Y')
        )
        payment9.save()

        payment10 = Payment(
            user=self.user,
            loan=Loan.objects.get(pk=1),
            payment='missed',
            amount=150.94,
            date=datetime.strptime('18082019', '%d%m%Y')
        )
        payment10.save()

        payment11 = Payment(
            user=self.user,
            loan=Loan.objects.get(pk=1),
            payment='made',
            amount=150.94,
            date=datetime.strptime('18092019', '%d%m%Y')
        )
        payment11.save()

        payment12 = Payment(
            user=self.user,
            loan=Loan.objects.get(pk=1),
            payment='made',
            amount=150.94,
            date=datetime.strptime('18102019', '%d%m%Y')
        )
        payment12.save()

        loan_data14 = {
            'client': 1,
            'amount': 300,
            'term': 2,
            'rate': 0.05,
        }
        response = self.client.post('/loans/', data=loan_data14, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
