import json
from datetime import datetime
from django.test import TestCase 
from django.urls import reverse, resolve 
from rest_framework import status
from api.views import payments, clients, loans
from django.contrib.auth.models import User
from api.models import Client, Loan, Payment
from api.serializers import ClientSerializer, LoanSerializer, PaymentSerializer


class PaymentTest(TestCase):

    def setUp(self):
        self.date = datetime.now()

        # Create user
        user = User.objects.create_user(
            username='usuario', email='usuario@email.com', password='pass'
        )
        self.client.login(username='usuario', password='pass')
          
        # Create a client
        Client.objects.create(user=user, name='Marcelo', surname='Mileris', email='marcelo.mileris@gmail.com', 
            telephone='19981308867', cpf='323.692.958-80')
        Client.objects.create(user=user, name='João', surname='da Silva', email='joaosilva@hotmail.com', 
            telephone='19874536958', cpf='123.654.987-90')
        # Create a loan
        c1 = Client.objects.get(name='Marcelo')
        c2 = Client.objects.get(name='João')
        l1 = Loan.objects.create(user=user, client=c1, amount='1000', term=12, rate=0.05, installment=85.60, date= self.date)        
        l2 = Loan.objects.create(user=user, client=c2, amount='1500', term=10, rate=0.05, installment=141.52, date= self.date)
        # Create a payment
        Payment.objects.create(user=user, loan=l1, payment='made', date=self.date, amount=470.8)
        Payment.objects.create(user=user, loan=l1, payment='made', date=self.date, amount=470.8)
        Payment.objects.create(user=user, loan=l1, payment='missed', date=self.date, amount=85.6)
        Payment.objects.create(user=user, loan=l2, payment='missed', date=self.date, amount=141.52)

    def test_get_payments(self):
        response = self.client.get(reverse('payments', kwargs={'pk': 1}))
        payments = Payment.objects.filter(loan_id=1).values()
        serializer = PaymentSerializer(payments, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_payment(self):
        data_send = json.dumps({"payment":"made", "date": "2019-05-19T11:24:00", "amount": "85.60"})
        response = self.client.post(reverse('payments', kwargs={'pk':1}), data_send, content_type='application/json')
        payments = Payment.objects.latest('id')
        serializer = PaymentSerializer(payments)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    