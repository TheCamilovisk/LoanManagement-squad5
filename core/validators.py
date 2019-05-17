from django.core.exceptions import ValidationError

def validate_term(term):
    if term <= 0:
        raise ValidationError(
            'Number of terms has to be a positive integer number.'
            )


def validate_amount(amount):
    if amount <= 0:
        raise ValidationError(
            'Amount has to be a positive real number.'
        )
