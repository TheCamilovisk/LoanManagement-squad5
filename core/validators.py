from django.core.exceptions import ValidationError

def validate_amount(amount):
    if amount <= 0:
        raise ValidationError('Amount has to be a positive real number.')