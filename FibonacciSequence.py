# Calculating the Fibonacci sequence 
#(Defining a function to calculate Fibonacci sequence with specific lenght)

import numpy as np

def FibonacciSequence (SeqLenght):
    FibSeqArray = np.zeros(SeqLenght+1)
    for i in range (SeqLenght+1):
        if i == 0:
            FibSeqArray[i] = 0
        elif i == 1:
            FibSeqArray[i] = 1
        else:
            for i in range (2,SeqLenght+1):
                FibSeqArray[i] = FibSeqArray[i-1]+FibSeqArray[i-2]
    FibSeqArray = np.delete(FibSeqArray, 0)
    return FibSeqArray

print (FibonacciSequence(10))

#FibSeqArray = np.zeros(10)
#for i in range (10):
#    if i == 0:
#        FibSeqArray[i] = 0
#    elif i == 1:
#        FibSeqArray[i] = 1
#    else:
#        for i in range (2,10):
#            FibSeqArray[i] = FibSeqArray[i-1]+FibSeqArray[i-2]
#FibSeqArray = np.delete(FibSeqArray, 0)