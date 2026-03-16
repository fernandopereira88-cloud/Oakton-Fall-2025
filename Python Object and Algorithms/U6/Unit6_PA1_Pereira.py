'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/02/2025
############################################################################################################################
ASSIGNMENT: Karatsuba Algorithm
================================================================================================================================================================================================================        
'''
import random 
def perform_karatsuba_multiplication(x: int,y: int):
    '''
    Description: A recursive implementation of the Karatsuba multiplication using base 2 (as per the assignment description)
    Inputs:
        - x: one of the integers to be multiplied
        - y: another of the integers to be multiplied
    Outputs:
        - Returns the result of multiplying two integers
    '''
    # Base case
    if x < 2 or y < 2:
        return x*y
    
    n = max(x.bit_length(),y.bit_length())
    
    m = n // 2
    
    x1 = x >> m
    x2 = x & ((1 << m)-1)
    y1 = y >> m
    y2 = y & ((1 << m)-1)
    
    # Recursive multiplications
    x1y1 = perform_karatsuba_multiplication(x1,y1)
    x2y2 = perform_karatsuba_multiplication(x2,y2)
    x1x2y1y2 = perform_karatsuba_multiplication(x1 + x2, y1 + y2)
    
    # Middle term [(Xleft-half + Xright-half)*(Yleft-half + Yright-half) - Xleft-half*Yleft-half - Xright-half*Yright-half]
    x1x2Plusy1y2 = x1x2y1y2 - x1y1 - x2y2
    
    return (x1y1<<(2*m)) + (x1x2Plusy1y2<<m) + x2y2
    

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
    
    print(f"KARATSUBA MULTIPLICATION --> X: {int1:,.0f} and Y: {int2:,.0f}. Multiplication Result: {perform_karatsuba_multiplication(int1,int2):,.0f}")
    
    
    
if __name__ == "__main__":
    main()