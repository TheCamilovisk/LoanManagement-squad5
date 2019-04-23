# Loan Management System

## Objective
The main objective of this project is to create an API to manage the loan payments control system from a fintech.

## Purpose
The purpose of this challenge is to test your ability to implement a solution given an abstract problem. You may find a problem in the asked task that you need to explain the problem and propose a solution to fix it.

## Problem
A fintech needs to keep track of the amount of money loaned and the missed/made payments. It also needs a place to retrieve the volume of outstanding debt at some point in time.

## Limitations
Loans are paid back in monthly installments.

## Endpoints
### POST /loans
**Summary**
Create a loan application. Loans are automatically accepted.

**Payload**
* amount: loan amount in dollars.
* term: number of months that will take until the loan gets paid-off.
* rate: interest rate as decimal.
* date: when the loan was requested (origination date as an ISO 8601 string).

**Example of sent data**
<pre><code>
{
  "amount": 1000,
  "term": 12,
  "rate": 0.05,
  "date": "2019-05-09 03:18Z"
}
</pre></code>
 
**Reply**
* loan_id: unique id of the loan.
* installment: monthly loan payment.
 
**Example of received data**
<pre><code>
{
  "loan_id": "000-0000-0000-0000"
  "installment": 85.60
}
</pre></code>
 
**Notes**
Loan payment formula
 
<pre><code>
r = rate / 12
installment = [r + r / ((1 + r) ^ term - 1)] x amount
</pre></code>

**Example**
For repaying a loan of $1000 at 5% interest for 12 months, the equation would be:
<pre><code>
installment = [(0.05 / 12) + (0.05 / 12) / ((1 + (0.05 / 12)) ^ 12 - 1] x 1000
installment = 85.60
</pre></code>

### POST /loans/<:id>/payments
**Summary**
Create a record of a payment made or missed.

**Payload**
* payment: type of payment: made or missed.
* date: payment date.
* amount: amount of the payment made or missed in dollars.

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
* date: loan balance until this date.
**Example of sent data**
<pre><code>
{
    "date": "2017-09-05 02:18Z"
}
</pre></code>

**Reply**
* balance: outstanding debt of loan.
**Example**
<pre><code>
{
    "balance": 40
}
</pre></code>
