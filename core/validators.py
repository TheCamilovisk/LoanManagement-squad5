from datetime import datetime
from django.core.exceptions import ValidationError
import re
from datetime import datetime


def validate_term(term):
    if term <= 0:
        raise ValidationError("Number of terms has to be a positive integer number.")


def validate_rate(rate):
    if rate < 0.03 or rate > 1:
        raise ValidationError('Rate should be between 0.03 and 1')


def validate_amount(amount):
    if amount <= 0:
        raise ValidationError("Amount has to be a positive real number.")


class CPFValidator:
    pattern = re.compile(r"^[\d]{11}$")

    def __call__(self, cpf):
        if self.pattern.match(cpf) is None or cpf == "00000000000":
            raise ValidationError("The given CPF is invalid.")

        cpf = [int(element) for element in cpf]

        for digit_i in (9, 10):
            upper_b = digit_i + 1
            modulus = (
                sum((i * num for i, num in zip(range(upper_b, 1, -1), cpf[:digit_i])))
                * 10
            ) % 11
            modulus = 0 if modulus == 10 or modulus == 11 else modulus
            if modulus != cpf[digit_i]:
                raise ValidationError("The given CPF is invalid.")


def validate_telephone(telephone):
    if re.compile(r"^[\d]{11}$").match(telephone) is None:
        raise ValidationError("The given telephone is invalid.")


def validate_payment(payment):
    if len(payment) > 6:
        raise ValidationError("check if the type of payment is correct")
    elif payment not in ("made", "missed"):
        raise ValidationError('type of payment should by "made" or "missed"')


def validate_date(date):
    date = date.strftime("%Y-%m-%dT%H:%Mz")
    # Validate the format
    try:
        datetime.strptime(date, "%Y-%m-%dT%H:%Mz")
    except ValueError:
        raise ValidationError('date should by in format ISO 8601 "YYYY-mm-ddTH:Mz"')

    # Validate the current date
    date = datetime.strptime(date, "%Y-%m-%dT%H:%Mz").date()
    current = datetime.now().date()
    if date != current:
        raise ValidationError("the date can not be different from the current date")
