from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Client, Loan, Payment
from core.serializers import PaymentSerializer, PaymentCreateSerializer
from core.validators import *
from core.views import *
from rest_framework.test import APIClient
from django.http import HttpRequest


class PaymentTest(TestCase):
    def setUp(self):
        self.date = datetime.now()
        date = datetime.strftime(self.date, "%Y-%m-%dT%H:%M")
        self.data_send = {"payment": "made", "date": f"{date}", "amount": "85.60"}

        # Create user
        self.user = User.objects.create_user(
            username="usuario", email="usuario@email.com", password="pass"
        )
        self.user.save()

        # Create a client
        self.c1 = Client.objects.create(
            user=self.user,
            name="Marcelo",
            surname="Mileris",
            email="marcelo.mileris@gmail.com",
            telephone="19981308867",
            cpf="32369295880",
        )

        # Create a loan
        self.l1 = Loan.objects.create(
            user=self.user,
            client=self.c1,
            amount="1000",
            term=12,
            rate=0.05,
            installment=85.60,
            date=self.date,
        )
        self.l1.save()
        self.p1 = Payment.objects.create(user=self.user, loan=self.l1, amount=900, date=self.date, payment='made')
        self.p1.save()

    def test_get_payments(self):
        url = reverse("api-jwt-auth")
        resp = self.client.post(
            url, {"username": "usuario", "password": "pass"}, format="json"
        )
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.get(reverse("payments", kwargs={"pk": 1}))
        payments = Payment.objects.filter(loan_id=1).values()
        serializer = PaymentSerializer(payments, many=True)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_payment(self):
        url = reverse("api-jwt-auth")
        resp = self.client.post(
            url, {"username": "usuario", "password": "pass"}, format="json"
        )
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.post(
            reverse("payments", kwargs={"pk": 1}), data=self.data_send, format="json"
        )
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_400(self):
        url = reverse("api-jwt-auth")
        resp = self.client.post(
            url, {"username": "usuario", "password": "pass"}, format="json"
        )
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.post(
            reverse("payments", kwargs={"pk": 10}), data=self.data_send, format="json"
        )
        self.assertEqual(response.data, "{'loan not found'}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_value_incorrect(self):
        self.date = datetime.now()
        date = datetime.strftime(self.date, "%Y-%m-%dT%H:%M")
        self.data_send = {"payment": "made", "date": f"{date}", "amount": "85.61"}
        url = reverse("api-jwt-auth")
        resp = self.client.post(
            url, {"username": "usuario", "password": "pass"}, format="json"
        )
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.post(
            reverse("payments", kwargs={"pk": 1}), data=self.data_send, format="json"
        )
        self.assertEqual(response.data, "{'value of payment is incorrect'}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_value_above(self):
        p1 = Payment.objects.create(user=self.user, loan=self.l1, amount=990, date=self.date, payment='made')
        p1.save()
        date = datetime.now()
        date = datetime.strftime(date, "%Y-%m-%dT%H:%M")
        data_send = {"payment": "made", "date": f"{date}", "amount": "85.60"}
        url = reverse("api-jwt-auth")
        resp = self.client.post(
            url, {"username": "usuario", "password": "pass"}, format="json"
        )
        token = resp.data["token"]
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.post(
            reverse("payments", kwargs={"pk": 1}), data=data_send, format="json"
        )
        self.assertEqual(response.data, "{'it is not possible to pay a value above the loan amount'}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validator_payment(self):
        try:
            payment = 'missedd'
            validate_payment(payment)
        
        except ValidationError as e:
            self.assertEqual(e.message, "check if the type of payment is correct")

        try:
            payment = 'mace'
            validate_payment(payment)
        except ValidationError as e:
            self.assertEqual(e.message, 'type of payment should by "made" or "missed"')

    def test_validator_date(self):
        date = datetime.now()
        try:           
            validate_date(datetime(date.year,date.month,date.day,date.hour,date.minute, date.second))
        except ValidationError as e:
            self.assertEqual(e.message, 'date should by in format ISO 8601 "YYYY-mm-ddTH:M"')

        try:
            validate_date(datetime(date.year,date.month,date.day-1,date.hour,date.minute))  
        except ValidationError as e:
            self.assertEqual(e.message, "the date can not be different from the current date") 

    def payment_calc(self):
        date = datetime.now()
        date = datetime.strftime(date, "%Y-%m-%dT%H:%M")
        data_send = {"payment": "made", "date": f"{date}", "amount": "85.60"}
        request = HttpRequest()
        request.data = data_send
        loan = self.l1        
        res = payment_calc(loan, request, 1)
        self.assertEqual(res, False)