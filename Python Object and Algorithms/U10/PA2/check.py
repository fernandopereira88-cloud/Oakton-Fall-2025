import time
import random
from concurrent.futures import ThreadPoolExecutor, wait

# -----------------------------
# Utility functions
# -----------------------------

def zero_matrix(n):
    return [[0.0 for _ in range(n)] for _ in range(n)]

def random_matrix(n, low=0, high=10):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]

def copy_matrix(M):
    n = len(M)
    return [row[:] for row in M]

def matrices_equal(A, B, eps=1e-6):
    n = len(A)
    for i in range(n):
        for j in range(n):
            if abs(A[i][j] - B[i][j]) > eps:
                return False
    return True

# -----------------------------
# 1) Generic (iterative) O(n^3)
# -----------------------------

def matmul_generic(A, B):
    n = len(A)
    C = zero_matrix(n)
    for i in range(n):
        for k in range(n):       # good cache behavior
            aik = A[i][k]
            for j in range(n):
                C[i][j] += aik * B[k][j]
    return C

# -----------------------------
# Shared recursive kernel (block-based)
# -----------------------------
# A, B, C are full matrices, we work on sub-blocks given by indices.

def recursive_block(A, B, C, n, ar, ac, br, bc, cr, cc):
    # Multiply sub-block A[ar:ar+n][ac:ac+n] by B[br:br+n][bc:bc+n]
    # and accumulate into C[cr:cr+n][cc:cc+n]
    if n == 1:
        C[cr][cc] += A[ar][ac] * B[br][bc]
        return

    new = n // 2

    # Block coordinates:
    # A11: (ar, ac), A12: (ar, ac+new), A21: (ar+new, ac), A22: (ar+new, ac+new)
    # B11: (br, bc), ...
    # C11: (cr, cc), ...
    # C11 = A11*B11 + A12*B21
    recursive_block(A, B, C, new, ar, ac, br, bc, cr, cc)                 # A11 * B11
    recursive_block(A, B, C, new, ar, ac + new, br + new, bc, cr, cc)     # A12 * B21

    # C12 = A11*B12 + A12*B22
    recursive_block(A, B, C, new, ar, ac, br, bc + new, cr, cc + new)     # A11 * B12
    recursive_block(A, B, C, new, ar, ac + new, br + new, bc + new,
                    cr, cc + new)                                         # A12 * B22

    # C21 = A21*B11 + A22*B21
    recursive_block(A, B, C, new, ar + new, ac, br, bc, cr + new, cc)     # A21 * B11
    recursive_block(A, B, C, new, ar + new, ac + new, br + new, bc,
                    cr + new, cc)                                         # A22 * B21

    # C22 = A21*B12 + A22*B22
    recursive_block(A, B, C, new, ar + new, ac, br, bc + new,
                    cr + new, cc + new)                                   # A21 * B12
    recursive_block(A, B, C, new, ar + new, ac + new, br + new, bc + new,
                    cr + new, cc + new)                                   # A22 * B22

def matmul_recursive(A, B):
    n = len(A)
    C = zero_matrix(n)
    recursive_block(A, B, C, n, 0, 0, 0, 0, 0, 0)
    return C

# -----------------------------
# Strassen serial
# -----------------------------

def add_block(X, xr, xc, Y, yr, yc, Z, zr, zc, n):
    for i in range(n):
        for j in range(n):
            Z[zr + i][zc + j] = X[xr + i][xc + j] + Y[yr + i][yc + j]

def sub_block(X, xr, xc, Y, yr, yc, Z, zr, zc, n):
    for i in range(n):
        for j in range(n):
            Z[zr + i][zc + j] = X[xr + i][xc + j] - Y[yr + i][yc + j]

def strassen_block(A, B, C, n, ar, ac, br, bc, cr, cc, cutoff=1):
    # cutoff: below this size, fall back to regular recursive_block
    if n <= cutoff:
        recursive_block(A, B, C, n, ar, ac, br, bc, cr, cc)
        return

    if n == 1:
        C[cr][cc] += A[ar][ac] * B[br][bc]
        return

    new = n // 2

    # Allocate S1..S10 and P1..P7 as full matrices, but we only use [0:new][0:new]
    def tmp():
        return zero_matrix(new)
    S1 = tmp(); S2 = tmp(); S3 = tmp(); S4 = tmp(); S5 = tmp()
    S6 = tmp(); S7 = tmp(); S8 = tmp(); S9 = tmp(); S10 = tmp()
    P1 = tmp(); P2 = tmp(); P3 = tmp(); P4 = tmp()
    P5 = tmp(); P6 = tmp(); P7 = tmp()

    # Compute S1..S10
    # S1 = B12 - B22
    sub_block(B, br, bc + new, B, br + new, bc + new, S1, 0, 0, new)
    # S2 = A11 + A12
    add_block(A, ar, ac, A, ar, ac + new, S2, 0, 0, new)
    # S3 = A21 + A22
    add_block(A, ar + new, ac, A, ar + new, ac + new, S3, 0, 0, new)
    # S4 = B21 - B11
    sub_block(B, br + new, bc, B, br, bc, S4, 0, 0, new)
    # S5 = A11 + A22
    add_block(A, ar, ac, A, ar + new, ac + new, S5, 0, 0, new)
    # S6 = B11 + B22
    add_block(B, br, bc, B, br + new, bc + new, S6, 0, 0, new)
    # S7 = A12 - A22
    sub_block(A, ar, ac + new, A, ar + new, ac + new, S7, 0, 0, new)
    # S8 = B21 + B22
    add_block(B, br + new, bc, B, br + new, bc + new, S8, 0, 0, new)
    # S9 = A11 - A21
    sub_block(A, ar, ac, A, ar + new, ac, S9, 0, 0, new)
    # S10 = B11 + B12
    add_block(B, br, bc, B, br, bc + new, S10, 0, 0, new)

    # Compute P1..P7 recursively
    # P1 = A11 * S1
    strassen_block(A, S1, P1, new, ar, ac, 0, 0, 0, 0, cutoff)
    # P2 = S2 * B22
    strassen_block(S2, B, P2, new, 0, 0, br + new, bc + new, 0, 0, cutoff)
    # P3 = S3 * B11
    strassen_block(S3, B, P3, new, 0, 0, br, bc, 0, 0, cutoff)
    # P4 = A22 * S4
    strassen_block(A, S4, P4, new, ar + new, ac + new, 0, 0, 0, 0, cutoff)
    # P5 = S5 * S6
    strassen_block(S5, S6, P5, new, 0, 0, 0, 0, 0, 0, cutoff)
    # P6 = S7 * S8
    strassen_block(S7, S8, P6, new, 0, 0, 0, 0, 0, 0, cutoff)
    # P7 = S9 * S10
    strassen_block(S9, S10, P7, new, 0, 0, 0, 0, 0, 0, cutoff)

    # Combine into C
    for i in range(new):
        for j in range(new):
            # C11 = C11 + P5 + P4 - P2 + P6
            C[cr + i][cc + j] += P5[i][j] + P4[i][j] - P2[i][j] + P6[i][j]
            # C12 = C12 + P1 + P2
            C[cr + i][cc + j + new] += P1[i][j] + P2[i][j]
            # C21 = C21 + P3 + P4
            C[cr + i + new][cc + j] += P3[i][j] + P4[i][j]
            # C22 = C22 + P5 + P1 - P3 - P7
            C[cr + i + new][cc + j + new] += P5[i][j] + P1[i][j] - P3[i][j] - P7[i][j]

def matmul_strassen(A, B, cutoff=32):
    n = len(A)
    C = zero_matrix(n)
    strassen_block(A, B, C, n, 0, 0, 0, 0, 0, 0, cutoff=cutoff)
    return C

# -----------------------------
# Parallel recursive
# -----------------------------

def parallel_recursive_block(A, B, C, n, ar, ac, br, bc, cr, cc, executor, depth=0, max_depth=1):
    """Parallel recursive multiply.
    Only at levels with depth < max_depth do we spawn threads for the 8 subcalls.
    """
    if n == 1:
        C[cr][cc] += A[ar][ac] * B[br][bc]
        return

    new = n // 2

    if depth >= max_depth:
        # just use serial recursion below cutoff depth
        recursive_block(A, B, C, n, ar, ac, br, bc, cr, cc)
        return

    # Temporary D for the second group of products
    D = zero_matrix(n)

    futures = []

    # T1..T4 accumulate directly into C
    futures.append(executor.submit(
        parallel_recursive_block, A, B, C, new, ar, ac, br, bc, cr, cc, executor, depth+1, max_depth))
    futures.append(executor.submit(
        parallel_recursive_block, A, B, C, new, ar, ac, br, bc + new, cr, cc + new, executor, depth+1, max_depth))
    futures.append(executor.submit(
        parallel_recursive_block, A, B, C, new, ar + new, ac, br, bc, cr + new, cc, executor, depth+1, max_depth))
    futures.append(executor.submit(
        parallel_recursive_block, A, B, C, new, ar + new, ac, br, bc + new, cr + new, cc + new, executor, depth+1, max_depth))

    # T5..T8 accumulate into D
    futures.append(executor.submit(
        parallel_recursive_block, A, B, D, new, ar, ac + new, br + new, bc, 0, 0, executor, depth+1, max_depth))
    futures.append(executor.submit(
        parallel_recursive_block, A, B, D, new, ar, ac + new, br + new, bc + new, 0, new, executor, depth+1, max_depth))
    futures.append(executor.submit(
        parallel_recursive_block, A, B, D, new, ar + new, ac + new, br + new, bc, new, 0, executor, depth+1, max_depth))
    futures.append(executor.submit(
        parallel_recursive_block, A, B, D, new, ar + new, ac + new, br + new, bc + new, new, new, executor, depth+1, max_depth))

    wait(futures)

    # Combine D into C
    for i in range(n):
        for j in range(n):
            C[cr + i][cc + j] += D[i][j]

def matmul_recursive_parallel(A, B, max_depth=1, max_workers=8):
    n = len(A)
    C = zero_matrix(n)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        parallel_recursive_block(A, B, C, n, 0, 0, 0, 0, 0, 0, executor, depth=0, max_depth=max_depth)
    return C

# -----------------------------
# Parallel Strassen
# -----------------------------

def parallel_strassen_block(A, B, C, n, ar, ac, br, bc, cr, cc,
                            executor, depth=0, max_depth=1, cutoff=32):
    if n <= cutoff:
        # Use serial recursive multiplication at small sizes
        recursive_block(A, B, C, n, ar, ac, br, bc, cr, cc)
        return

    if n == 1:
        C[cr][cc] += A[ar][ac] * B[br][bc]
        return

    new = n // 2

    def tmp():
        return zero_matrix(new)
    S1 = tmp(); S2 = tmp(); S3 = tmp(); S4 = tmp(); S5 = tmp()
    S6 = tmp(); S7 = tmp(); S8 = tmp(); S9 = tmp(); S10 = tmp()
    P1 = tmp(); P2 = tmp(); P3 = tmp(); P4 = tmp()
    P5 = tmp(); P6 = tmp(); P7 = tmp()

    # Compute S1..S10 (can be parallelized too, but we keep it simple)
    sub_block(B, br, bc + new, B, br + new, bc + new, S1, 0, 0, new)
    add_block(A, ar, ac, A, ar, ac + new, S2, 0, 0, new)
    add_block(A, ar + new, ac, A, ar + new, ac + new, S3, 0, 0, new)
    sub_block(B, br + new, bc, B, br, bc, S4, 0, 0, new)
    add_block(A, ar, ac, A, ar + new, ac + new, S5, 0, 0, new)
    add_block(B, br, bc, B, br + new, bc + new, S6, 0, 0, new)
    sub_block(A, ar, ac + new, A, ar + new, ac + new, S7, 0, 0, new)
    add_block(B, br + new, bc, B, br + new, bc + new, S8, 0, 0, new)
    sub_block(A, ar, ac, A, ar + new, ac, S9, 0, 0, new)
    add_block(B, br, bc, B, br, bc + new, S10, 0, 0, new)

    if depth >= max_depth:
        # Below max_depth, just use serial Strassen
        strassen_block(A, B, C, n, ar, ac, br, bc, cr, cc, cutoff=cutoff)
        return

    futures = []

    # P1 = A11 * S1
    futures.append(executor.submit(
        parallel_strassen_block, A, S1, P1, new, ar, ac, 0, 0, 0, 0,
        executor, depth+1, max_depth, cutoff))
    # P2 = S2 * B22
    futures.append(executor.submit(
        parallel_strassen_block, S2, B, P2, new, 0, 0, br + new, bc + new, 0, 0,
        executor, depth+1, max_depth, cutoff))
    # P3 = S3 * B11
    futures.append(executor.submit(
        parallel_strassen_block, S3, B, P3, new, 0, 0, br, bc, 0, 0,
        executor, depth+1, max_depth, cutoff))
    # P4 = A22 * S4
    futures.append(executor.submit(
        parallel_strassen_block, A, S4, P4, new, ar + new, ac + new, 0, 0, 0, 0,
        executor, depth+1, max_depth, cutoff))
    # P5 = S5 * S6
    futures.append(executor.submit(
        parallel_strassen_block, S5, S6, P5, new, 0, 0, 0, 0, 0, 0,
        executor, depth+1, max_depth, cutoff))
    # P6 = S7 * S8
    futures.append(executor.submit(
        parallel_strassen_block, S7, S8, P6, new, 0, 0, 0, 0, 0, 0,
        executor, depth+1, max_depth, cutoff))
    # P7 = S9 * S10
    futures.append(executor.submit(
        parallel_strassen_block, S9, S10, P7, new, 0, 0, 0, 0, 0, 0,
        executor, depth+1, max_depth, cutoff))

    wait(futures)

    # Combine into C
    for i in range(new):
        for j in range(new):
            C[cr + i][cc + j] += P5[i][j] + P4[i][j] - P2[i][j] + P6[i][j]
            C[cr + i][cc + j + new] += P1[i][j] + P2[i][j]
            C[cr + i + new][cc + j] += P3[i][j] + P4[i][j]
            C[cr + i + new][cc + j + new] += P5[i][j] + P1[i][j] - P3[i][j] - P7[i][j]

def matmul_strassen_parallel(A, B, max_depth=1, max_workers=8, cutoff=32):
    n = len(A)
    C = zero_matrix(n)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        parallel_strassen_block(A, B, C, n, 0, 0, 0, 0, 0, 0,
                                executor, depth=0, max_depth=max_depth, cutoff=cutoff)
    return C

# -----------------------------
# Benchmarking
# -----------------------------

def time_function(fn, *args, repeats=3):
    # Return min runtime over 'repeats' runs
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn(*args)
        end = time.perf_counter()
        best = min(best, end - start)
    return best

def main():
    # Choose sizes (powers of two for recursive/Strassen)
    sizes = [16, 32, 64, 128, 256, 512, 1024, 2048]   # you can add 256, 512 if your machine is fast enough

    print("SERIAL RUNTIMES (seconds)")
    print("{:>6} {:>12} {:>12} {:>12}".format("n", "Generic", "Recursive", "Strassen"))
    for n in sizes:
        A = random_matrix(n)
        B = random_matrix(n)

        t_generic = time_function(matmul_generic, A, B)
        t_rec = time_function(matmul_recursive, A, B)
        t_strassen = time_function(matmul_strassen, A, B)

        print("{:>6} {:>12.6f} {:>12.6f} {:>12.6f}".format(
            n, t_generic, t_rec, t_strassen))

    print("\nPARALLEL RUNTIMES (seconds)")
    print("{:>6} {:>12} {:>12}".format("n", "Rec_Par", "Strassen_Par"))
    for n in sizes:
        A = random_matrix(n)
        B = random_matrix(n)

        t_rec_par = time_function(matmul_recursive_parallel, A, B)
        t_str_par = time_function(matmul_strassen_parallel, A, B)

        print("{:>6} {:>12.6f} {:>12.6f}".format(
            n, t_rec_par, t_str_par))

if __name__ == "__main__":
    main()
