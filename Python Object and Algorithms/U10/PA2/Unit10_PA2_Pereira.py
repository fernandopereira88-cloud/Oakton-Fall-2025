'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/09/2025
############################################################################################################################
ASSIGNMENT: Parallel Matrix Multiplication

ASSIGNMENT QUESTIONS:
In your report, include answers to the following questions [2 points each; 10 points]:

1) What values of n do we see any improvement in runtime using the parallel approach compared to the serial approach?
    - The performance between serial and parallel algorithms up to n=90 is very similar, but, serial algorithms performed faster most of the time.    
    - Parallel Recursive had better runtimes for n equalled 22, 32, 52, 62, and 82
    - Parallel Strassen improves runtime when n equalled 22, 32, and 82
    
===============================
= RUNTIME REPORT (in seconds) =
===============================
n       | Sequential Generic    | Sequential Recursive  | Parallel Recursive    | Sequential Strassen's | Parallel Strassen's   |
2       | 0.000002              | 0.000007              | 0.000019              | 0.000015              | 0.000025              |
12      | 0.000105              | 0.000493              | 0.000504              | 0.002769              | 0.003057              |
22      | 0.000794              | 0.003872              | 0.003656              | 0.019497              | 0.019338              |
32      | 0.001907              | 0.004032              | 0.003905              | 0.019784              | 0.019499              |
42      | 0.004692              | 0.029787              | 0.030453              | 0.137778              | 0.141248              |
52      | 0.008967              | 0.031639              | 0.030103              | 0.136649              | 0.138315              |
62      | 0.014148              | 0.031903              | 0.030652              | 0.134346              | 0.136795              |
72      | 0.024067              | 0.226843              | 0.226915              | 0.892676              | 0.924311              |
82      | 0.035027              | 0.231562              | 0.230082              | 0.958465              | 0.942299              |
92      | 0.049538              | 0.233640              | 0.238250              | 0.909116              | 0.952934              |

2) Why does the generic algorithm outperform the recursive algorithm in most cases?
    - Both are O(n^3), but the recursive algorithm generates more memory overhead to keep up with recursions, causing additional inefficiencies

3) What values of n allow for Strassen's Algorithm to outperform the recursive algorithm?
    - for the n values measured above, the Strassen’s is consistently slower than the standard recursive algorithm.
    
4) Why does the parallel recursive matrix multiplication algorithm use temporary matrix D?
    - D is used to allow recursive calls to run in parallel

5) Explain in simple terms how the recursive matrix multiplication algorithm works.
    - The Base case happens when the partitioned matrices have only one element. In this case, elements are mutliplied and added to their address in the final matrix.
    - In the recursive case, each matrix is split in 4 partitioned matrices of size n/2 (half the original size), and, then, tested to the base case
    - Once the recursion is completed, the partitioned resulting matrices of C should have their elements updated, 
      so all is needed at that point is to aggregate the matrix back to its original size by adding the appropriate elements together.

############################################################################################################################
############################################################################################################################
'''

from concurrent.futures import ThreadPoolExecutor,wait
import time
import math
import random

#########################
# SEQUENTIAL ALGORITHMS #
#########################
##########################
# GENERIC MULTIPLICATION #
##########################
def matrix_multiplication(matrixA,matrixB,matrixC,n):
    '''
    Description: Generic matrix multiplication algorithm    
    Inputs:
        - matrixA: The input matrix A (left side of the matrix multiplication)
        - matrixB: The input matrix B (right side of the matrix multiplication)
        - matrixC: Initially filled with zeros, this matrix will be updated with the multiplications between A and B matrices.
    Outputs:
        - None returned to the user, but will update elements in matrixC to represent the matrix product between A and B
    '''
    for i in range(n):
        for j in range(n):
            for k in range(n):
                matrixC[i][j] += matrixA[i][k]*matrixB[k][j]

def prep_recursive_matrix_multiplication(matrixA,matrixB):
    '''
    Description: 
        - Prepare input matrices A and B for the recursive algorithm and calls the recursive algorithm
    Inputs:
        - matrixA: The input matrix A (left side of the matrix multiplication)
        - matrixB: The input matrix B (right side of the matrix multiplication)
    Outputs:
        - matrixC: the output matrix with the calculated terms for A x B
    '''
    n = len(matrixA)
    
    # Adjustments to support when n is odd
    m =1 if n == 1 else 2**math.ceil(math.log2(n))    
    matrixA_pad = [[0] * m for _ in range(m)]
    matrixB_pad = [[0] * m for _ in range(m)]
    for i in range(n):
        for j in range(n):
            matrixA_pad[i][j] = matrixA[i][j]
            matrixB_pad[i][j] = matrixB[i][j]
    
    matrixC_pad = [[0] * m for _ in range(m)]
    
    recursive_matrix_multiplication(matrixA_pad,matrixB_pad,matrixC_pad,m,
                                    a_row=0,a_col=0,
                                    b_row=0,b_col=0,
                                    c_row=0,c_col=0)
    
    matrixC = [[matrixC_pad[i][j] for j in range(n)] for i in range(n)]
    
    return matrixC

############################
# RECURSIVE MULTIPLICATION #
############################
def recursive_matrix_multiplication(matrixA,matrixB,matrixC,n,a_row,a_col,b_row,b_col,c_row,c_col):
    '''
    Description: Algorithm to calculate the product of two square matrices using recursion
    Inputs:
        - matrixA: The input matrix A (left side of the matrix multiplication)
        - matrixB: The input matrix B (left side of the matrix multiplication)
        - matrixC: Initially filled with zeros, this matrix will be updated with the multiplications between A and B matrices.
        - n : the number of rows or cols (it's a square matrix, so those are the same)
        - a_row: helper to partition matrix A row during recursion
        - a_col: helper to partition matrix A column during recursion
        - b_row: helper to partition matrix B row during recursion
        - b_col: helper to partition matrix B column during recursion
        - c_row: helper to partition matrix C row during recursion
        - c_col: helper to partition matrix C column during recursion
        
    Outputs:
        - None returned to the user, but will update elements in matrixC (padded) to represent the matrix product between A and B
    '''
    
    if n == 1:
        # --Base case: multiply single elements
        matrixC[c_row][c_col] = matrixC[c_row][c_col] + matrixA[a_row][a_col]*matrixB[b_row][b_col]
        return
    
    # Create partitions
    mid = n // 2
    
    # Conquer
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row,a_col,
                                    b_row,b_col,
                                    c_row,c_col)
    
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row,a_col+mid,
                                    b_row+mid,b_col,
                                    c_row,c_col)
    
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row,a_col,
                                    b_row,b_col+mid,
                                    c_row,c_col+mid)
    
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row,a_col+mid,
                                    b_row+mid,b_col+mid,
                                    c_row,c_col+mid)    
    
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row+mid,a_col,
                                    b_row,b_col,
                                    c_row+mid,c_col)    
    
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row+mid,a_col+mid,
                                    b_row+mid,b_col,
                                    c_row+mid,c_col)    
    
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row+mid,a_col,
                                    b_row,b_col+mid,
                                    c_row+mid,c_col+mid)
    
    recursive_matrix_multiplication(matrixA,matrixB,matrixC,mid,
                                    a_row+mid,a_col+mid,
                                    b_row+mid,b_col+mid,
                                    c_row+mid,c_col+mid)        

#############################
# STRASSEN'S MULTIPLICATION #
#############################

# helper functions
def partition_matrix(matrixM):
    '''
    Description: helper function to partition a matrix M in smaller matrices half its size
    Inputs:
        - matrixM: the matrix to be partitioned
    Outputs:
        - The partitioned matrices matrixM11, matrixM12, matrixM21, matrixM22
    '''
    n = len(matrixM)
    mid = n // 2
    matrixM11 = [row[:mid] for row in matrixM[:mid]]
    matrixM12 = [row[mid:] for row in matrixM[:mid]]
    matrixM21 = [row[:mid] for row in matrixM[mid:]]
    matrixM22 = [row[mid:] for row in matrixM[mid:]]
    
    return matrixM11, matrixM12, matrixM21, matrixM22

def add_matrix(matrixA,matrixB):
    '''
    Description: Performs a matricial addition between A and B (A + B)
    Inputs:
        - matrixA: The input matrix A (left side of the matrix addition)
        - matrixB: The input matrix B (right side of the matrix addition)
    Outputs:
        - Returns a list of lists with the matrix  that represents the substracted matrix
    '''
    n = len(matrixA)
    return [[matrixA[i][j] + matrixB[i][j] for j in range(n)] for i in range(n)]

def sub_matrix(matrixA,matrixB):
    '''
    Description: Performs a matricial subtraction between A and B (A - B)
    Inputs:
        - matrixA: The input matrix A (left side of the matrix subtraction)
        - matrixB: The input matrix B (right side of the matrix subtraction)
    Outputs:
        - Returns a list of lists with the matrix  that represents the substracted matrix
    '''
    n = len(matrixA)
    return [[matrixA[i][j] - matrixB[i][j] for j in range(n)] for i in range(n)]
    
def zero_matrix(n):
    '''
    Description: creates a NxN matrix with 0s to help in the Strassen's multiplication
    Inputs:
        - n: matrix length
    Outputs:
        - Returns a list of lists with the matrix 
    '''
    return [[0 for _ in range(n)] for _ in range(n)]

def strassens_matrix_multiplication(matrixA,matrixB,matrixC,n):
    '''
    Description: Algorithm to calculate the product of two square matrices using recursion
    Inputs:
        - matrixA: The input matrix A (left side of the matrix multiplication)
        - matrixB: The input matrix B (right side of the matrix multiplication)
        - matrixC: Initially filled with zeros, this matrix will be updated with the multiplications between A and B matrices.
        - n : the number of rows or cols (it's a square matrix, so those are the same)
        
    Outputs:
        - None returned to the user, but will update elements in matrixC (padded) to represent the matrix product between A and B
    '''
    if n == 1:
        matrixC[0][0] += matrixA[0][0] * matrixB[0][0]
        return
    
    matrixA11, matrixA12, matrixA21, matrixA22 = partition_matrix(matrixA)
    matrixB11, matrixB12, matrixB21, matrixB22 = partition_matrix(matrixB)
    matrixC11, matrixC12, matrixC21, matrixC22 = partition_matrix(matrixC)
    
    new_size = n//2
    
    matrixS1 = sub_matrix(matrixB12,matrixB22)
    matrixS2 = add_matrix(matrixA11,matrixA12)
    matrixS3 = add_matrix(matrixA21,matrixA22)
    matrixS4 = sub_matrix(matrixB21,matrixB11)
    matrixS5 = add_matrix(matrixA11,matrixA22)
    matrixS6 = add_matrix(matrixB11,matrixB22)
    matrixS7 = sub_matrix(matrixA12,matrixA22)
    matrixS8 = add_matrix(matrixB21,matrixB22)
    matrixS9 = sub_matrix(matrixA11,matrixA21)
    matrixS10 = add_matrix(matrixB11,matrixB12)

    matrixP1 = zero_matrix(new_size)
    matrixP2 = zero_matrix(new_size)
    matrixP3 = zero_matrix(new_size)
    matrixP4 = zero_matrix(new_size)
    matrixP5 = zero_matrix(new_size)
    matrixP6 = zero_matrix(new_size)
    matrixP7 = zero_matrix(new_size)
    
    strassens_matrix_multiplication(matrixA11, matrixS1,  matrixP1, new_size)
    strassens_matrix_multiplication(matrixS2,  matrixB22, matrixP2, new_size)
    strassens_matrix_multiplication(matrixS3,  matrixB11, matrixP3, new_size)
    strassens_matrix_multiplication(matrixA22, matrixS4,  matrixP4, new_size)
    strassens_matrix_multiplication(matrixS5,  matrixS6,  matrixP5, new_size)
    strassens_matrix_multiplication(matrixS7,  matrixS8,  matrixP6, new_size)
    strassens_matrix_multiplication(matrixS9,  matrixS10, matrixP7, new_size)
    
    for i in range(new_size):
        for j in range(new_size):
            matrixC[i][j]                   += matrixP5[i][j] + matrixP4[i][j] - matrixP2[i][j] + matrixP6[i][j]
            matrixC[i][j+new_size]          += matrixP1[i][j] + matrixP2[i][j]
            matrixC[i+new_size][j]          += matrixP3[i][j] + matrixP4[i][j]
            matrixC[i+new_size][j+new_size] += matrixP5[i][j] + matrixP1[i][j] - matrixP3[i][j] - matrixP7[i][j]

def prep_strassen_multiplication(matrixA,matrixB):
    '''    
    Description: 
        - Prepare input matrices A and B for the Strassen's multiplication algorithm 
    Inputs:
        - matrixA: The input matrix A (left side of the matrix multiplication)
        - matrixB: The input matrix B (right side of the matrix multiplication)
    Outputs:
        - matrixC: the output matrix with the calculated terms for A x B
    '''    
    
    n = len(matrixA)
    
    # Treatment for when n is odd    
    m = 1 if n == 0 else 2 ** math.ceil(math.log2(n))
    
    matrixA_pad = [[0] * m for _ in range(m)]
    matrixB_pad = [[0] * m for _ in range(m)]
    for i in range(n):
        for j in range(n):
            matrixA_pad[i][j] = matrixA[i][j]
            matrixB_pad[i][j] = matrixB[i][j]
    
    matrixC_pad = [[0] * m for _ in range(m)]
    
    strassens_matrix_multiplication(matrixA_pad,matrixB_pad,matrixC_pad,m)
    
    matrixC = [[matrixC_pad[i][j] for j in range(n)] for i in range(n)]
    
    return matrixC

#######################
# PARALLEL ALGORITHMS #
#######################
# RECURSIVE ALGORITHM #
# --- CONFIG: -------------------------------------------------------
MAX_WORKERS = 8          # max number of worker threads
PARALLEL_CUTOFF = 64     # below this n, run recursion sequentially
# -------------------------------------------------------------------

def prep_recursive_matrix_multiplication_parallel(matrixA, matrixB):
    '''
    Description: Parallel algorithm version of prep_recursive_matrix_multiplication.
    Inputs:
        - matrixA: The input matrix A (left side of the matrix multiplication)
        - matrixB: The input matrix B (right side of the matrix multiplication)
    Outputs:
        - matrixC: the output matrix with the calculated terms for A x B
    '''    
    n = len(matrixA)

    # Adjustments to support when n is odd
    m = 1 if n == 1 else 2 ** math.ceil(math.log2(n))
    matrixA_pad = [[0] * m for _ in range(m)]
    matrixB_pad = [[0] * m for _ in range(m)]
    for i in range(n):
        for j in range(n):
            matrixA_pad[i][j] = matrixA[i][j]
            matrixB_pad[i][j] = matrixB[i][j]

    matrixC_pad = [[0] * m for _ in range(m)]

    # Use a ThreadPoolExecutor and pass it down the recursion
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        recursive_matrix_multiplication_parallel(
            matrixA_pad, matrixB_pad, matrixC_pad, m,
            a_row=0, a_col=0,
            b_row=0, b_col=0,
            c_row=0, c_col=0,
            executor=executor,
        )

    # Remove padding
    matrixC = [[matrixC_pad[i][j] for j in range(n)] for i in range(n)]
    return matrixC

def recursive_matrix_multiplication_parallel(matrixA, matrixB, matrixC, n,
                                             a_row, a_col,
                                             b_row, b_col,
                                             c_row, c_col,
                                             executor=None):
    '''
    Description: Algorithm to calculate the product of two square matrices using recursion AND PARALLEL approach
    Inputs:
        - matrixA: The input matrix A (left side of the matrix multiplication)
        - matrixB: The input matrix B (left side of the matrix multiplication)
        - matrixC: Initially filled with zeros, this matrix will be updated with the multiplications between A and B matrices.
        - n : the number of rows or cols (it's a square matrix, so those are the same)
        - a_row: helper to partition matrix A row during recursion
        - a_col: helper to partition matrix A column during recursion
        - b_row: helper to partition matrix B row during recursion
        - b_col: helper to partition matrix B column during recursion
        - c_row: helper to partition matrix C row during recursion
        - c_col: helper to partition matrix C column during recursion
        - executor: execution support to spawn and coordinate parallel tasks in the algorithm
        
    Outputs:
        - None returned to the user, but will update elements in matrixC (padded) to represent the matrix product between A and B
    '''    
    
   # Base case
    if n == 1:
        matrixC[c_row][c_col] += matrixA[a_row][a_col] * matrixB[b_row][b_col]
        return

    # For small n or no executor: fall back to existing *sequential* recursion
    # to avoid excess thread overhead.
    if executor is None or n <= PARALLEL_CUTOFF:
        recursive_matrix_multiplication(
            matrixA, matrixB, matrixC, n,
            a_row, a_col,
            b_row, b_col,
            c_row, c_col
        )
        return

    new_size = n // 2

    # Temporary matrix D of size n 
    D = [[0] * n for _ in range(n)]

    futures = []

    # ----- T1–T4: contribute directly into C's four quadrants -----
    # T1: C11 += A11 * B11
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, matrixC, new_size,
        a_row, a_col,          # A11
        b_row, b_col,          # B11
        c_row, c_col,          # C11
        executor
    ))

    # T2: C12 += A11 * B12
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, matrixC, new_size,
        a_row, a_col,          # A11
        b_row, b_col + new_size,  # B12
        c_row, c_col + new_size,  # C12
        executor
    ))

    # T3: C21 += A21 * B11
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, matrixC, new_size,
        a_row + new_size, a_col,  # A21
        b_row, b_col,             # B11
        c_row + new_size, c_col,  # C21
        executor
    ))

    # T4: C22 += A21 * B12
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, matrixC, new_size,
        a_row + new_size, a_col,          # A21
        b_row, b_col + new_size,          # B12
        c_row + new_size, c_col + new_size,  # C22
        executor
    ))

    # ----- T5–T8: second products into D (no races with C) -----
    # We'll treat D as a full n×n matrix and use its 4 quadrants:
    #   D11: rows [0..new_size-1],       cols [0..new_size-1]
    #   D12: rows [0..new_size-1],       cols [new_size..n-1]
    #   D21: rows [new_size..n-1],       cols [0..new_size-1]
    #   D22: rows [new_size..n-1],       cols [new_size..n-1]

    # T5: D11 += A12 * B21
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, D, new_size,
        a_row, a_col + new_size,        # A12
        b_row + new_size, b_col,        # B21
        0, 0,                           # D11
        executor
    ))

    # T6: D12 += A12 * B22
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, D, new_size,
        a_row, a_col + new_size,        # A12
        b_row + new_size, b_col + new_size,  # B22
        0, new_size,                    # D12
        executor
    ))

    # T7: D21 += A22 * B21
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, D, new_size,
        a_row + new_size, a_col + new_size,  # A22
        b_row + new_size, b_col,             # B21
        new_size, 0,                         # D21
        executor
    ))

    # T8: D22 += A22 * B22
    futures.append(executor.submit(
        recursive_matrix_multiplication_parallel,
        matrixA, matrixB, D, new_size,
        a_row + new_size, a_col + new_size,  # A22
        b_row + new_size, b_col + new_size,  # B22
        new_size, new_size,                  # D22
        executor
    ))

    # Wait for all 8 tasks
    wait(futures)

    # Finally, combine D into C for this block:
    # C[c_row + i][c_col + j] += D[i][j]
    for i in range(n):
        Ci = c_row + i
        for j in range(n):
            Cj = c_col + j
            matrixC[Ci][Cj] += D[i][j]
        
# STRASSEN's ALGORITHM #
def strassens_matrix_multiplication_parallel(matrixA,
                                             matrixB,
                                             matrixC,
                                             n,
                                             executor,
                                             depth=0,
                                             max_depth=3):
    '''
    Parallel version of Strassen's multiplication.
    INputs:    
        - executor : ThreadPoolExecutor instance shared across recursive calls.
        - depth    : current recursion depth.
        - max_depth: controls the level of parallelization for the seven matrix operations subcalls (P1 to P7).
                Deeper levels will run sequentially to avoid overhead.
    Outputs:
        - None returned to the user, but will update elements in matrixC (padded) to represent the matrix product between A and B    
    '''
    # Base case
    if n == 1:
        matrixC[0][0] += matrixA[0][0] * matrixB[0][0]
        return

    
    matrixA11, matrixA12, matrixA21, matrixA22 = partition_matrix(matrixA)
    matrixB11, matrixB12, matrixB21, matrixB22 = partition_matrix(matrixB)
    matrixC11, matrixC12, matrixC21, matrixC22 = partition_matrix(matrixC)

    new_size = n // 2

    matrixS1  = sub_matrix(matrixB12, matrixB22)
    matrixS2  = add_matrix(matrixA11, matrixA12)
    matrixS3  = add_matrix(matrixA21, matrixA22)
    matrixS4  = sub_matrix(matrixB21, matrixB11)
    matrixS5  = add_matrix(matrixA11, matrixA22)
    matrixS6  = add_matrix(matrixB11, matrixB22)
    matrixS7  = sub_matrix(matrixA12, matrixA22)
    matrixS8  = add_matrix(matrixB21, matrixB22)
    matrixS9  = sub_matrix(matrixA11, matrixA21)
    matrixS10 = add_matrix(matrixB11, matrixB12)

    
    matrixP1 = zero_matrix(new_size)
    matrixP2 = zero_matrix(new_size)
    matrixP3 = zero_matrix(new_size)
    matrixP4 = zero_matrix(new_size)
    matrixP5 = zero_matrix(new_size)
    matrixP6 = zero_matrix(new_size)
    matrixP7 = zero_matrix(new_size)

    # Decide whether to parallelize this level
    use_parallel = (depth < max_depth) and (n > PARALLEL_CUTOFF)

    if use_parallel:    
        # Launch the 7 recursive multiplications in parallel
        futures = []
        futures.append(executor.submit(strassens_matrix_multiplication_parallel,
                                       matrixA11, matrixS1,  matrixP1, new_size,
                                       executor, depth + 1, max_depth))
        futures.append(executor.submit(strassens_matrix_multiplication_parallel,
                                       matrixS2,  matrixB22, matrixP2, new_size,
                                       executor, depth + 1, max_depth))
        futures.append(executor.submit(strassens_matrix_multiplication_parallel,
                                       matrixS3,  matrixB11, matrixP3, new_size,
                                       executor, depth + 1, max_depth))
        futures.append(executor.submit(strassens_matrix_multiplication_parallel,
                                       matrixA22, matrixS4,  matrixP4, new_size,
                                       executor, depth + 1, max_depth))
        futures.append(executor.submit(strassens_matrix_multiplication_parallel,
                                       matrixS5,  matrixS6,  matrixP5, new_size,
                                       executor, depth + 1, max_depth))
        futures.append(executor.submit(strassens_matrix_multiplication_parallel,
                                       matrixS7,  matrixS8,  matrixP6, new_size,
                                       executor, depth + 1, max_depth))
        futures.append(executor.submit(strassens_matrix_multiplication_parallel,
                                       matrixS9,  matrixS10, matrixP7, new_size,
                                       executor, depth + 1, max_depth))

        # Wait for all to finish
        for f in futures:
            f.result()
    else:
        # BSequential fall back
        strassens_matrix_multiplication_parallel(matrixA11, matrixS1,  matrixP1, new_size,
                                                 executor, depth + 1, max_depth)
        strassens_matrix_multiplication_parallel(matrixS2,  matrixB22, matrixP2, new_size,
                                                 executor, depth + 1, max_depth)
        strassens_matrix_multiplication_parallel(matrixS3,  matrixB11, matrixP3, new_size,
                                                 executor, depth + 1, max_depth)
        strassens_matrix_multiplication_parallel(matrixA22, matrixS4,  matrixP4, new_size,
                                                 executor, depth + 1, max_depth)
        strassens_matrix_multiplication_parallel(matrixS5,  matrixS6,  matrixP5, new_size,
                                                 executor, depth + 1, max_depth)
        strassens_matrix_multiplication_parallel(matrixS7,  matrixS8,  matrixP6, new_size,
                                                 executor, depth + 1, max_depth)
        strassens_matrix_multiplication_parallel(matrixS9,  matrixS10, matrixP7, new_size,
                                                 executor, depth + 1, max_depth)

    
    for i in range(new_size):
        for j in range(new_size):
            matrixC[i][j]                   += matrixP5[i][j] + matrixP4[i][j] - matrixP2[i][j] + matrixP6[i][j]
            matrixC[i][j + new_size]        += matrixP1[i][j] + matrixP2[i][j]
            matrixC[i + new_size][j]        += matrixP3[i][j] + matrixP4[i][j]
            matrixC[i + new_size][j+new_size] += matrixP5[i][j] + matrixP1[i][j] - matrixP3[i][j] - matrixP7[i][j]


def prep_strassen_multiplication_parallel(matrixA, matrixB, max_workers=None, max_depth=3):
    '''
    Description: Parallel version of prep_strassen_multiplication(). Used to prepare input matrices and run parallel Strassen's multiplication.

    Inputs:
        - max_workers: number of threads in the pool (None is default).
        - max_depth  : how deep the recursion uses parallelism.
    Outputs:
        - matrixC: the output matrix with the calculated terms for A x B        
    '''
    n = len(matrixA)

    # Handle non power-of-two size by padding
    m = 1 if n == 0 else 2 ** math.ceil(math.log2(n))

    matrixA_pad = [[0] * m for _ in range(m)]
    matrixB_pad = [[0] * m for _ in range(m)]
    for i in range(n):
        for j in range(n):
            matrixA_pad[i][j] = matrixA[i][j]
            matrixB_pad[i][j] = matrixB[i][j]

    matrixC_pad = [[0] * m for _ in range(m)]

    # Create a shared thread pool and kick off the top-level call
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        strassens_matrix_multiplication_parallel(matrixA_pad,
                                                 matrixB_pad,
                                                 matrixC_pad,
                                                 m,
                                                 executor,
                                                 depth=0,
                                                 max_depth=max_depth)

    # Remove padding
    matrixC = [[matrixC_pad[i][j] for j in range(n)] for i in range(n)]
    return matrixC

def generate_square_matrix(n):
    '''
    Description: generates an NxN matrix with random integers betwen 0 and 1,234,567
    
    Inputs:
        - n: the matrix size
    Outputs:
        - a list of lists representing the matrix
        
    '''
    matrix = [[random.randint(0,1234567) for j in range(n)] for i in range(n)]
    return matrix

def perform_and_compare_multiplications(n):
    '''
    Description:
        - Docstring for perform_and_compare_multiplications
    Inputs:
        - n: the matrix size
    Outputs:
        - None returned to the user, but will print the duration for each algorithm
    '''
    # matrixA = [[4,6],[7,-1]]
    # matrixB = [[2,5],[4,-8]]

    matrixA = generate_square_matrix(n)
    matrixB = generate_square_matrix(n)
    matrixC = [[0]*n for i in range(n)]
    
    # print(matrixA)
    # Sequential Algorithms
    # Sequential generic
    start = time.time()
    matrix_multiplication(matrixA=matrixA,matrixB=matrixB,matrixC=matrixC,n=n)
    end = time.time()
    duration1 = end - start
    
    
    # Recursive
    matrixC.clear()
    matrixC = [[0]*n for i in range(n)]
    start = time.time()
    matrixC = prep_recursive_matrix_multiplication(matrixA,matrixB)
    end = time.time()
    duration2 = end - start
    
        
    # Strassen
    matrixC.clear()
    matrixC = [[0]*n for i in range(n)]
    start = time.time()
    matrixC = prep_strassen_multiplication(matrixA,matrixB)
    end = time.time()
    duration3 = end - start
    
    
    # Parallel Algorithms
    # Recursive
    matrixC.clear()
    matrixC = [[0]*n for i in range(n)]
    start = time.time()
    matrixC = prep_recursive_matrix_multiplication_parallel(matrixA,matrixB)
    end = time.time()
    duration4 = end - start    
    
        
    # Strassen
    matrixC.clear()
    matrixC = [[0]*n for i in range(n)]
    start = time.time()
    matrixC = prep_strassen_multiplication_parallel(matrixA,matrixB)
    end = time.time()
    duration5 = end - start    

    string_results = f"{n}\t| {duration1:,.6f}\t\t| {duration2:,.6f}\t\t| {duration4:,.6f}\t\t| {duration3:,.6f}\t\t| {duration5:,.6f}\t\t|"    
    
    print(string_results)
    
    
def main():    
    '''
    Description: driver program that calls the method to execute different matrix multiplication calculations
    Inputs:
        - None form the user
    Outputs:
        - Generates a report with runtime performance for different matrix sizes
    '''
    print("===============================")
    print("= RUNTIME REPORT (in seconds) =")
    print("===============================")
    string_header = "n\t| Sequential Generic\t| Sequential Recursive\t| Parallel Recursive\t| Sequential Strassen's\t| Parallel Strassen's   |"
    print(string_header)
    
    for i in range(2,102,10):
        perform_and_compare_multiplications(i)
    

    
if __name__ == "__main__":
    main()