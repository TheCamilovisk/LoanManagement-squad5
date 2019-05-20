from django.core.exceptions import ValidationError
import re
from datetime import datetime


def validate_term(term):
    if term <= 0:
        raise ValidationError('Number of terms has to be a positive integer number.')


def validate_rate(rate):
    if rate < 0.03 or rate > 1:
        raise ValidationError('Rate should be between 0.03 and 1')


def validate_amount(amount):
    if amount <= 0:
        raise ValidationError('Amount has to be a positive real number.')


def validate_cpf(cpf):
    if re.compile(r'^[\d]{11}$').match(cpf) is None or cpf == '00000000000':
        raise ValidationError('The given CPF is invalid.')

    modulus = (
        sum((i * int(element) for i, element in zip(range(10, 1, -1), cpf[:9]))) * 10
    ) % 11
    if modulus == 10 or modulus == 11:
        modulus = 0
    if modulus != int(cpf[9]):
        raise ValidationError('The given CPF is invalid.')

    modulus = (
        sum((i * int(element) for i, element in zip(range(11, 1, -1), cpf[:10]))) * 10
    ) % 11
    if modulus == 10 or modulus == 11:
        modulus = 0
    if modulus != int(cpf[10]):
        raise ValidationError('The given CPF is invalid.')


def validate_telephone(telephone):
    if re.compile(r'^[\d]{11}$').match(telephone) is None:
        raise ValidationError('The given telephone is invalid.')


      
def validate_payment(payment):
    if (len(payment) > 6):
        raise ValidationError('check if the type of payment is correct')
    elif (payment not in ('made', 'missed')):
        raise ValidationError('type of payment should by "made" or "missed"')


def validate_date(date):
    date = date.strftime('%Y-%m-%dT%H:%Mz')
    # Validate the format
    try:
        datetime.strptime(date, '%Y-%m-%dT%H:%Mz')
    except ValueError:
       raise ValidationError('date should by in format ISO 8601 "YYYY-mm-ddTH:Mz"')

    # Validate the current date
    try:
        date = datetime.strptime(date, '%Y-%m-%dT%H:%Mz').date()
        current = datetime.now().date()
        if (date != current):
            raise ValidationError('the date can not be different from the current date')
    except ValueError:
        raise ValidationError('the date can not be different from the current date')
