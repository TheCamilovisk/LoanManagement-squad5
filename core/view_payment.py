def payments(request, pk, format=None):
    if request.method == 'GET':
        payments = Payment.objects.filter(loan_id=pk).values()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':

        serializer = PaymentCreateSerializer(data=request.data)
        if serializer.is_valid():

            dt = datetime.strptime(request.data['date'], '%Y-%m-%dT%H:%M')
            year = dt.year
            month = dt.month
            payd_month = Payment.objects.filter(created__month=month, created__year=year)
            
            if (payd_month):
                return Response({'error': 'it is not possible to make two payments in the month'}, 
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                loan = Loan.objects.get(id=pk)
                installment = round(loan.installment, 2)
                term = round(loan.term, 2)
                
                amount = float(request.data['amount'])
                payment = request.data['payment']
                
                loan_total = round((installment*term), 2)
                loan_paid = Payment.objects.filter(loan_id=pk, payment='made').aggregate(Sum('amount'))['amount__sum'] or 0.00            
                loan_paid = round(loan_paid + amount, 2)

                if (installment == amount):                
                    if (loan_paid > loan_total):
                        return Response({'error': 'it is not possible to pay a value above the loan amount'}, 
                            status=status.HTTP_400_BAD_REQUEST)   
                    elif (loan_paid == loan_total):
                        serializer.save(user=request.user, loan=loan)
                        loan.paid = True
                        loan.save()                
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        serializer.save(user=request.user, loan=loan)              
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error:', 'value of payment is incorrect'})
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        payments = Payment.objects.filter(loan_id=pk)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
