'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/08/2025
############################################################################################################################
ASSIGNMENT: Parallel Karatsuba

ASSIGNMENT QUESTIONS:

1) Find the runtimes of the following product for both versions of the Karatsuba algorithm: 123,456,789 * 123,456,789. [3 points]
    - According to the one time runtime report, the parallel algorithm is 34x slower than the sequential algorithm
##################
# Runtime report #
##################    
KARATSUBA MULTIPLICATION SEQUENTIAL     --> X: 123,456,789 and Y: 123,456,789. Multiplication Result: 15,241,578,750,190,520. Duration: 0.000080s
KARATSUBA MULTIPLICATION PARALLEL       --> X: 123,456,789 and Y: 123,456,789. Multiplication Result: 15,241,578,750,190,520. Duration: 0.001759s

2) Explain when this parallel scheme maximizes the CPU usage on your system? [3 points]
    - CPU usage will be maximized when 3 CPU cores are available to perform the P1, P2, and P3 tasks for the multipplication, and when multiplying very large numbers, as the initial setup operational cost is amortized by the recursion.
    
3) What are the disadvantages of this parallel scheme? Provide an example of this disadvantage and explain? [4 points]
    - The main disadvantage of this parallel scheme is the fixed setup required to initialize the parallel algorithm through ThreadPoolExecutor as it create algorithm overhead. 
    - In the Karatsuba algorithm this disadvantage, for example, the ThreadPoolExecutor is created and 3 tasks are submitted. 
    - As the algorithm is not working with a very large amount of data and both the sequential and parallel versions are very fast, the overhead generated creates inefficiencies at this level and makes the parallel algorithm significanlty slower.
    - In addition, parallel algorithms can create bottlenecks when a portion of the algorithm completes before another as the computer needs to sync and capture all relevant inputs before moving forward.
    
############################################################################################################################
############################################################################################################################
'''

from concurrent.futures import ThreadPoolExecutor
import time

def perform_karatsuba_multiplication_sequential(x: int,y: int):
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
    x1y1 = perform_karatsuba_multiplication_sequential(x1,y1)
    x2y2 = perform_karatsuba_multiplication_sequential(x2,y2)
    x1x2y1y2 = perform_karatsuba_multiplication_sequential(x1 + x2, y1 + y2)
    
    # Middle term [(Xleft-half + Xright-half)*(Yleft-half + Yright-half) - Xleft-half*Yleft-half - Xright-half*Yright-half]
    x1x2Plusy1y2 = x1x2y1y2 - x1y1 - x2y2
    
    return (x1y1<<(2*m)) + (x1x2Plusy1y2<<m) + x2y2
    
def perform_karatsuba_multiplication_parallel(x: int,y: int):
    '''
    Description: A recursive implementation of the Karatsuba multiplication using base 2 (as per the assignment description) using parallel approach through multi threads
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

    
    # Splitting factors
    x1 = x >> m
    x2 = x & ((1 << m)-1)
    y1 = y >> m
    y2 = y & ((1 << m)-1)
    
    
    # Create executor    
    with ThreadPoolExecutor(max_workers=3) as executor:
        tasks =[
            executor.submit(perform_karatsuba_multiplication_sequential, x1, y1),
            executor.submit(perform_karatsuba_multiplication_sequential, x2, y2),
            executor.submit(perform_karatsuba_multiplication_sequential, x1+x2, y1+y2)            
        ] 
        x1y1, x2y2, x1x2y1y2 = [task.result() for task in tasks]    
    
    # Middle term
    x1x2Plusy1y2 = x1x2y1y2 - x1y1 - x2y2
    
    return (x1y1<<(2*m)) + (x1x2Plusy1y2<<m) + x2y2
    
    
def main():
    '''
    Description: performs a Karatsuba multiplication sequential and parallel for 123456789*123456789 and displays a comparison of runtime
    Inputs:
        - None
    Outputs: 
        - Integer multiplication result
    '''
    int1 = 123456789
    int2 = 123456789
    
    start = time.time()
    karatsuba_sequential_result = perform_karatsuba_multiplication_sequential(int1,int2)
    end = time.time()
    karatsuba_sequential_duration = end - start
    
    print(f"KARATSUBA MULTIPLICATION SEQUENTIAL\t--> X: {int1:,.0f} and Y: {int2:,.0f}. Multiplication Result: {karatsuba_sequential_result:,.0f}. Duration: {karatsuba_sequential_duration:,.6f}s")
    

    start = time.time()
    karatsuba_parallel_result = perform_karatsuba_multiplication_parallel(int1,int2)
    end = time.time()
    karatsuba_parallel_duration = end - start
    
    print(f"KARATSUBA MULTIPLICATION PARALLEL\t--> X: {int1:,.0f} and Y: {int2:,.0f}. Multiplication Result: {karatsuba_parallel_result:,.0f}. Duration: {karatsuba_parallel_duration:,.6f}s")
    
if __name__ == "__main__":
    main()