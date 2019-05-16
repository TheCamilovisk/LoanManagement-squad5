from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return self.name + ' ' + self.surname


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    term = models.IntegerField()
    rate = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    installment = models.DecimalField(
        decimal_places=2, max_digits=10, blank=True, null=True
        )

    def __str__(self):
        return str(self.client) + " - " + str(self.date)


class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment = models.CharField(max_length=6)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.date) + ': ' + str(self.loan)
