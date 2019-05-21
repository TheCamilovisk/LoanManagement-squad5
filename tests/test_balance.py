from datetime import datetime

from django.contrib.auth.models import User
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core import views
from core.models import Loan, Payment


class BalanceTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="squad5user",
            email="squad5user@gmail.com",
            password="squad5userpass",
        )
        url = reverse("api-jwt-auth")
        resp = self.client.post(
            url, {"username": "squad5user", "password": "squad5userpass"}, format="json"
        )
        token = resp.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION="JWT " + token)

    def test_url_resolves_balance_view(self):
        """URL /loans/1/balance/ must use view balance"""
        view = resolve("/loans/1/balance/")
        self.assertEquals(view.func, views.balance)

    def test_balance_loan_paid(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712376",
        }
        self.client.post("/clients/", client_data, format="json")

        loan = {"client": 1, "amount": 1000, "term": 12, "rate": 0.05}
        self.client.post("/loans/", loan, format="json")

        for month in range(1, 13):
            p = Payment(
                loan=Loan.objects.get(pk=1),
                user=self.user,
                payment="made",
                date=datetime.strptime(f"10{month}2018", "%d%m%Y"),
                amount=Loan.objects.get(pk=1).installment,
            )
            p.save()

        response = self.client.get("/loans/1/balance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 0.00)

    def test_balance_loan_two_payments(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712376",
        }
        self.client.post("/clients/", client_data, format="json")

        loan = {"client": 1, "amount": 1000, "term": 12, "rate": 0.05}
        self.client.post("/loans/", loan, format="json")

        payment1 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment="made",
            date=datetime.strptime("10042019", "%d%m%Y"),
            amount=Loan.objects.get(pk=1).installment,
        )
        payment1.save()

        payment2 = Payment(
            loan=Loan.objects.get(pk=1),
            user=self.user,
            payment="made",
            date=datetime.strptime("10052019", "%d%m%Y"),
            amount=Loan.objects.get(pk=1).installment,
        )
        payment2.save()

        response = self.client.get("/loans/1/balance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 856.07)

    def test_balance_loan_without_payments(self):
        client_data = {
            "name": "Felicity",
            "surname": "Jones",
            "email": "felicity@gmail.com",
            "telephone": "11984345678",
            "cpf": "34598712376",
        }
        self.client.post("/clients/", client_data, format="json")

        loan = {"client": 1, "amount": 1000, "term": 12, "rate": 0.05}
        self.client.post("/loans/", loan, format="json")

        response = self.client.get("/loans/1/balance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 1027.29)

    def test_balance_loan_not_found(self):
        response = self.client.get("/loans/0/balance/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Loan not found")

    def test_balance_loan_invalid(self):
        response = self.client.get("/loans/a/balance/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
