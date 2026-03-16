import time
from concurrent.futures import ThreadPoolExecutor

# ----------------------------------------------------
# Utility: split an integer into binary halves (base 2)
# ----------------------------------------------------
def split_bits(x, m):
    """
    Split x into (high, low) where:
      x = high * 2^m + low
    """
    high = x >> m
    low = x & ((1 << m) - 1)
    return high, low


# ----------------------------------------------------
# Sequential Karatsuba (base 2)
# ----------------------------------------------------
def karatsuba_seq(x, y):
    # Base case: small numbers use direct multiply
    if x < 2 or y < 2:
        return x * y

    # Determine n = number of bits of largest operand
    n = max(x.bit_length(), y.bit_length())
    m = n // 2

    # Split each number into left and right halves
    xL, xR = split_bits(x, m)
    yL, yR = split_bits(y, m)

    # Karatsuba's 3 products
    P1 = karatsuba_seq(xL, yL)
    P2 = karatsuba_seq(xR, yR)
    P3 = karatsuba_seq(xL + xR, yL + yR)

    # Combine using the formula:
    # (2^n)*P1 + 2^(n/2)*[(P3 - P1) - P2] + P2
    mid = P3 - P1 - P2
    return (P1 << (2*m)) + (mid << m) + P2


# ----------------------------------------------------
# Parallel Karatsuba (3 threads per recursion)
# ----------------------------------------------------
def karatsuba_parallel(x, y, depth=0, max_depth=3, executor=None):
    # Base case
    if x < 2 or y < 2:
        return x * y

    n = max(x.bit_length(), y.bit_length())
    m = n // 2

    # If we've reached max depth, switch to sequential
    if depth >= max_depth:
        return karatsuba_seq(x, y)

    # Create executor on first call
    if executor is None:
        with ThreadPoolExecutor(max_workers=3) as ex:
            return karatsuba_parallel(x, y, depth, max_depth, ex)

    # Split operands (base-2 halves)
    xL, xR = split_bits(x, m)
    yL, yR = split_bits(y, m)

    # Spawn 3 tasks in parallel:
    f1 = executor.submit(karatsuba_parallel,
                         xL, yL, depth + 1, max_depth, executor)
    f2 = executor.submit(karatsuba_parallel,
                         xR, yR, depth + 1, max_depth, executor)
    f3 = executor.submit(karatsuba_parallel,
                         xL + xR, yL + yR, depth + 1, max_depth, executor)

    P1 = f1.result()
    P2 = f2.result()
    P3 = f3.result()

    mid = P3 - P1 - P2

    return (P1 << (2*m)) + (mid << m) + P2


# ----------------------------------------------------
# Test & timing
# ----------------------------------------------------
if __name__ == "__main__":
    a = 123456789
    b = 123456789

    # Convert to base-2 integers (already integers, but using bit_length for splitting)
    print("Correctness check:")
    seq = karatsuba_seq(a, b)
    par = karatsuba_parallel(a, b)
    built = a * b
    print("Sequential:", seq)
    print("Parallel:  ", par)
    print("Built-in:  ", built)
    print("Equal?", seq == par == built)
    print()

    print("Timing for 123,456,789 * 123,456,789:")
    t0 = time.time()
    karatsuba_seq(a, b)
    t1 = time.time()
    karatsuba_parallel(a, b)
    t2 = time.time()

    print(f"Sequential: {t1 - t0:.8f} sec")
    print(f"Parallel:   {t2 - t1:.8f} sec\n")
