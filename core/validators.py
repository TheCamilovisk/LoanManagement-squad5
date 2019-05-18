from django.core.exceptions import ValidationError
import re


def validate_term(term):
    if term <= 0:
        raise ValidationError('Number of terms has to be a positive integer number.')


def validate_amount(amount):
    if amount <= 0:
        raise ValidationError('Amount has to be a positive real number.')


def validate_cpf(cpf):
    if re.compile(r'^[\d]{11}$').match(cpf) is None or cpf == '00000000000':
        raise ValidationError('The given CPF is invalid.')
