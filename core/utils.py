def calc_installment(amount, term, rate):
    r = rate/term
    return (r + r / ((1 + r) ** term - 1)) * amount