'''
Created on May 1, 2024
This is a dynamic divide-and-conquer parallel multiplication algorithm.
float mult(float x, float y)

@author: Ivan Temesvari
'''
import time
from concurrent.futures import ThreadPoolExecutor

import multiprocessing

def mult_processes_parallel(x, y):
    # Find number of digits of x
    len_x = len(str(x))
    # Find number of digits of y
    len_y = len(str(y))
    if x < 10 or y < 10:
        return x * y
    else:
        # Divide up each number into four products
        # Get left half of x (x1) and right half of x (x2)
        x1 = x // (10 ** (len_x // 2))
        x2 = x % (10 ** (len_x // 2))
        # Get left half of y (y1) and right half of y (y2)
        y1 = y // (10 ** (len_y // 2))
        y2 = y % (10 ** (len_y // 2))

    with multiprocessing.Pool(processes=4) as pool:
        results = [
            pool.apply_async(mult, (x1, y1)),
            pool.apply_async(mult, (x1, y2)),
            pool.apply_async(mult, (x2, y2)),
            pool.apply_async(mult, (y1, x2))
        ]
        P1, P2, P3, P4 = [result.get() for result in results]

    return (P1 * 10 ** (len_x // 2 + len_y // 2) +
            P2 * 10 ** (len_x // 2) +
            P3 +
            P4 * 10 ** (len_y // 2))


def mult_threads(x, y):
    #Find number of digits of x.
    len_x = len(str(x))
    #Find number of digits of y.
    len_y = len(str(y))
    if x < 10 or y < 10:
        return x*y
    else:
        #Divide up each number into four products.
        #Get left half of x (x1) and right half of x (x2).
        x1 = x // (10 ** (len_x // 2))
        x2 = x % (10 ** (len_x // 2))
        #Get left half of y (y1) and right half of y (y2).
        y1 = y // (10 ** (len_y // 2))
        y2 = y % (10 ** (len_y // 2))
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [
            executor.submit(mult, x1, y1),
            executor.submit(mult, x1, y2),
            executor.submit(mult, x2, y2),
            executor.submit(mult, y1, x2)
        ]
        P1, P2, P3, P4 = [task.result() for task in tasks]
        
        
    return (P1 * 10 ** (len_x // 2 + len_y // 2) +
            P2 * 10 ** (len_x // 2) +
            P3 +
            P4 * 10 ** (len_y // 2))    
    
def mult(x, y):
    #Find number of digits of x.
    len_x = len(str(x))
    #Find number of digits of y.
    len_y = len(str(y))
    if x < 10 or y < 10:
        return x*y
    else:
        #Divide up each number into four products.
        #Get left half of x (x1) and right half of x (x2).
        x1 = x // (10 ** (len_x // 2))
        x2 = x % (10 ** (len_x // 2))
        #Get left half of y (y1) and right half of y (y2).
        y1 = y // (10 ** (len_y // 2))
        y2 = y % (10 ** (len_y // 2))

        return mult(x1, y1)*10**(len_x//2+len_y//2)\
                 + mult(x1, y2)*10**(len_x//2)\
                 + mult(x2, y2)\
                 + mult(y1, x2)*10**(len_y//2)
    
if __name__ == "__main__":
    x = 9248723412123456124343243245325566545454358769219834539434523453426435
    y = 6924126745567865434326657889774555534984502495486004038899837498372495
    
    #Approach to using multiple threads using concurrent.futures
    start_time = time.time()
    result = mult_threads(x, y)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time (parallel recursive threads):", execution_time, "seconds")
    print(result)
    
    #Non-parallel runtime.
    start_time = time.time()
    result = mult(x, y)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time (non-parallel recursive):", execution_time, "seconds")
    print(result)
    
    #Approach to using multiple processes using multiprocessing
    start_time = time.time()
    result = mult_processes_parallel(x, y)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time (multiprocessing recursive):", execution_time, "seconds")
    print(result)
    
    #Built-in python integer multiplication
    start_time = time.time()
    result = x*y
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time built-in:", execution_time, "seconds")
    print(result)