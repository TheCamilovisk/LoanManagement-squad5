from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Client, Loan, Payment
from core.serializers import PaymentSerializer, PaymentCreateSerializer
from rest_framework.test import APIClient


class PaymentTest(TestCase):
    def setUp(self):
        self.date = datetime.now()

        # Create user
        user = User.objects.create_user(
            username="usuario", email="usuario@email.com", password="pass"
        )
        user.save()

        # Create a client
        Client.objects.create(
            user=user,
            name="Marcelo",
            surname="Mileris",
            email="marcelo.mileris@gmail.com",
            telephone="19981308867",
            cpf="323.692.958-80",
        )
        Client.objects.create(
            user=user,
            name="João",
            surname="da Silva",
            email="joaosilva@hotmail.com",
            telephone="19874536958",
            cpf="123.654.987-90",
        )
        # Create a loan
        c1 = Client.objects.get(name="Marcelo")
        c2 = Client.objects.get(name="João")
        l1 = Loan.objects.create(
            user=user,
            client=c1,
            amount="1000",
            term=12,
            rate=0.05,
            installment=85.60,
            date=self.date,
        )
        l1.save()
        l2 = Loan.objects.create(
            user=user,
            client=c2,
            amount="1500",
            term=10,
            rate=0.05,
            installment=141.52,
            date=self.date,
        )
        l2.save()

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
        data_send = {"payment": "made", "date": "2019-05-20T11:24", "amount": "85.60"}

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
        self.assertEqual(response.data, {'detail': 'payment made successfully'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

