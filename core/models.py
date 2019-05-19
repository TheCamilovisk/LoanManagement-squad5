from django.db import models
from django.contrib.auth.models import User
from core import validators

class Base(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(Base):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telephone = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return self.name + ' ' + self.surname


class Loan(Base):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    amount = models.FloatField()
    term = models.IntegerField(validators=[validators.validate_term])
    rate = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    installment = models.FloatField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.client) + " - " + str(self.date)


class Payment(Base):
    loan = models.ForeignKey(Loan, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment = models.CharField(max_length=6,validators=[validators.validate_payment])
    date = models.DateTimeField(validators=[validators.validate_date])
    amount = models.DecimalField(decimal_places=2, max_digits=10, validators=[validators.validate_amount])

    def __str__(self):
        return str(self.date) + ': ' + str(self.loan)
