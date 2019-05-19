# Client and Loan Management System

[![Build Status](https://travis-ci.org/python-aceleradev-squad5/LoanManagement-squad5.svg?branch=master)](https://travis-ci.org/python-aceleradev-squad5/LoanManagement-squad5)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b035a0fd6a1bb4d6d9a/maintainability)](https://codeclimate.com/github/python-aceleradev-squad5/LoanManagement-squad5/maintainability)

## Objective
The main objective of this project is to create an API to manage clients and the loan payments control system from a fin-tech.

## Purpose
The purpose of this challenge is to test your ability to implement a solution given an abstract problem. You may find a problem in the asked task that you need to explain the problem and propose a solution to fix it.

## Problem
A fin-tech needs to create and manage the clients and keep track of the amount of money loaned and the missed/made payments. It also needs a place to retrieve the volume of outstanding debt at some point in time.

## Business Rules
* If a client contracted a loan in the past and paid all without missing any payment, you can decrease by 0.02% his tax rate.
* If a client contracted a loan in the past and paid all but missed until 3 monthly payments, you can increase by 0.04% his tax rate.
* If a client contracted a loan in the past and paid all but missed more than 3 monthly payments or didn’t pay all the loan, you need to deny the new one.

## Limitations
Loans are paid back in monthly installments.

## Endpoints
### POST /clients
**Summary**
Create a client in the system.

**Payload**
<pre><code>
name: the client's name.
surname: the client's surname.
email: the client's email.
telephone: the client's telephone.
cpf: the client's (Cadastro de Pessoa Física) identification.
</pre></code>

**Example of sent data**
<pre><code>
{
  "name": "Felicity",
  "surname": "Jones",
  "email": "felicity@gmail.com",
  "telephone": "11984345678",
  "cpf": "34598712387"
}
</pre></code>

**Reply**
<pre><code>
client_id: unique id of a client.
</pre></code>

**Example of received data**
<pre><code>
{
  "client_id": 1
} 
</pre></code>

### POST /loans
**Summary**
Create a loan application. Loans acceptance policies are described on the Business Rules above.

**Payload**
<pre><code>
client_id: the client's identification that contracted a loan.
amount: loan amount in dollars.
term: number of months that will take until the loan gets paid-off.
rate: interest rate as decimal.
date: when the loan was requested (origination date as an ISO 8601 string).
</pre></code>

**Example of sent data**
<pre><code>
{
  "client_id": 1,
  "amount": 1000,
  "term": 12,
  "rate": 0.05,
  "date": "2019-05-09 03:18Z"
}
</pre></code>
 
**Reply**
<pre><code>
loan_id: unique id of the loan.
installment: monthly loan payment.
</pre></code> 

**Example of received data**
<pre><code>
{
  "loan_id": "000-0000-0000-0000"
  "installment": 85.60
}
</pre></code>
 
**Notes**

_Loan payment formula_
 
<pre><code>
r = rate / term
installment = [r + r / ((1 + r) ^ term - 1)] x amount
</pre></code>

Example

For repaying a loan of $1000 at 5% interest for 12 months, the equation would be:
<pre><code>
installment = [(0.05 / 12) + (0.05 / 12) / ((1 + (0.05 / 12)) ^ 12 - 1] x 1000
installment = 85.60
</pre></code>

### POST /loans/<:id>/payments
**Summary**
Create a record of a payment made or missed.

**Payload**
<pre><code>
payment: type of payment: made or missed.
date: payment date.
amount: amount of the payment made or missed in dollars.
</pre></code>

**Example of sent data (Payment made)**
<pre><code>
{
  "payment": "made",
  "date": "2019-05-07 04:18Z",
  "amount": 85.60
}
</pre></code>

**Example of sent data (Payment missed)**
<pre><code>
{
  "payment": "missed",
  "date": "2019-05-07 04:18Z",
  "amount": 85.60
}
</pre></code>

### POST /loans/<:id>/balance
**Summary**
Get the volume of outstanding debt (i.e., debt yet to be paid) at some point in time.

**Payload**
<pre><code>
date: loan balance until this date.
</pre></code>

**Example of sent data**
<pre><code>
{
  "date": "2017-09-05 02:18Z"
}
</pre></code>

**Reply**
<pre><code>
balance: outstanding debt of loan.
</pre></code>

**Example**
<pre><code>
{
  "balance": 40
}
</pre></code>

## How to contribute

1. Clone the repository
2. Create a virtualenv with Python 3.7
3. Activate virtualenv
4. Install the dependencies
5. Configure the instance with .env
6. Run the tests

```console
git clone git@github.com:python-aceleradev-squad5/LoanManagement-squad5.git
cd LoanManagement-squad5
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```


## How to deploy

1. Create an heroku instance
2. Send settings to heroku
3. Set a secure secret key for the instance
4. Set DEBUG = False
5. Send the code to heroku

```console
heroku create minhainstancia
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku config:set DEBUG=False
git push heroku master --force
```

