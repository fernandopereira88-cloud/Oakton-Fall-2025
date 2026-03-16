'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/02/2025
############################################################################################################################
ASSIGNMENT: Karatsuba Algorithm
================================================================================================================================================================================================================        
'''
import random 
def perform_karatsuba_multiplication(x,y):
    '''
    Description: A recursive implementation of the Karatsuba multiplication
    Inputs:
        - x: one of the integers to be multiplied
        - y: another of the integers to be multiplied
    Outputs:
        - Returns the result of multiplying two integers
    '''
    # Base case
    if x < 10 or y < 10:
        return x*y
    
    xStr = str(x)
    yStr = str(y)
    
    lenX = len(xStr)
    lenY = len(yStr)
    
    n = max(lenX,lenY)
    
    m = n // 2
    
    x1 = x // (10**m)
    x2 = x %  (10**m)
    y1 = y // (10**m)
    y2 = y %  (10**m)
    
    # Recursive multiplications
    x1y1 = perform_karatsuba_multiplication(x1,y1)
    x2y2 = perform_karatsuba_multiplication(x2,y2)
    x1x2y1y2 = perform_karatsuba_multiplication(x1 + x2, y1 + y2)
    
    # Middle term [(Xleft-half + Xright-half)*(Yleft-half + Yright-half) - Xleft-half*Yleft-half - Xright-half*Yright-half]
    x1x2Plusy1y2 = x1x2y1y2 - x1y1 - x2y2
    
    return x1y1*(10**(2*m)) + x1x2Plusy1y2*(10**m) + x2y2
    

def main():
    '''
    Description: performs a Karatsuba multiplication for two random integers between 1 and 123456789 (inclusive)
    Inputs:
        - None
    Outputs: 
        - Integer multiplication result
    '''
    int1 = random.randint(1,123456789)
    int2 = random.randint(1,123456789)
    
    print(perform_karatsuba_multiplication(int1,int2))
    
    
    
if __name__ == "__main__":
    main()