from django.core.exceptions import ValidationError
from datetime import datetime

# Validators for loans
def validate_term(term):
    if term <= 0:
        raise ValidationError(
            'Number of terms has to be a positive integer number.'
            )


def validate_amount(amount):
    try:
        float(amount)
    except:
       raise ValidationError('the amount should by valid. i.e: 1000') 

    if amount <= 0:
        raise ValidationError(
            'Amount has to be a positive real number.'
        )


# Validators for payments
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
