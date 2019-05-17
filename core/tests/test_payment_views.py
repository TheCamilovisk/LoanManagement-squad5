import json
from datetime import datetime
from django.test import TestCase 
from django.urls import reverse, resolve 
from rest_framework import status
from core.views import payments, clients, loans
from core.models import Client, Loan, Payment
from core.api.serializers import ClientSerializer, LoanSerializer, PaymentSerializer


class PaymentTest(TestCase):

    def setUp(self):
        self.date = datetime.now()
        # Create a client
        Client.objects.create(name='Marcelo', surname='Mileris', email='marcelo.mileris@gmail.com', telephone='19981308867', cpf='323.692.958-80')
        Client.objects.create(name='João', surname='da Silva', email='joaosilva@hotmail.com', telephone='19874536958', cpf='123.654.987-90')
        # Create a loan
        c1 = Client.objects.get(name='Marcelo')
        c2 = Client.objects.get(name='João')
        l1 = Loan.objects.create(client=c1, amount='1000', term=12, rate=0.05, installment=85.60, date= self.date)        
        l2 = Loan.objects.create(client=c2, amount='1500', term=10, rate=0.05, installment=141.52, date= self.date)
        # Create a payment
        Payment.objects.create(loan=l1, payment='made', date=self.date, amount=85.60)
        Payment.objects.create(loan=l1, payment='made', date=self.date, amount=85.60)
        Payment.objects.create(loan=l2, payment='miss', date=self.date, amount=141.52)


    def test_get_payments(self):
        response = self.client.get(reverse('payments', kwargs={'pk': 1}))
        payments = Payment.objects.filter(loan_id=1).values()
        serializer = PaymentSerializer(payments, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_payment(self):
        data_send = json.dumps({"payment":"misseds", "date": "2019-05-16T11:24z", "amount": "85.60"})
        response = self.client.post(reverse('payments', kwargs={'pk':1}), data_send, content_type='application/json')
        payments = Payment.objects.latest('id')
        serializer = PaymentSerializer(payments)
        #self.assertEqual(response.data, serializer.data)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    '''
    def test_get_single_payment(self):
        response = self.client.get(reverse('payments', kwargs={'pk': 1}))      
        data = {"loan_id":1, "payment":"made", "date": "2019-05-16T11:24:08z", "amount": "85.60"}
        self.assertEqual(response.data, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_payment(self):
        data_send = json.dumps({"payment":"missed", "date": "2019-05-16T11:24:08z", "amount": "85.60"})
        data_res =  {"loan_id":1, "payment":"missed", "date": "2019-05-16T11:24:08z", "amount": "85.60"}
        response = self.client.post(reverse('payments', kwargs={'pk':1}), data_send, content_type='application/json')
        self.assertEqual(response.data, data_res)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    '''