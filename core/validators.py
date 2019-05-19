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
