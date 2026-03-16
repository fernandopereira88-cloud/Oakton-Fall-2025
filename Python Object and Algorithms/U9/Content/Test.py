# rsa_block_cipher.py

# =======================
# Basic Number Utilities
# =======================

def gcd(e, m):
    """Euclidean algorithm: returns gcd(e, m)."""
    x, y = e, m
    while y != 0:
        r = x % y
        x = y
        y = r
    return x


def modular_pow(base, exponent, modulus):
    """
    Naive modular exponentiation, exactly as in the assignment.
    Computes (base^exponent) mod modulus.
    """
    if modulus == 1:
        return 0
    c = 1
    for _ in range(exponent):
        c = (c * base) % modulus
    return c


def extended_gcd(e, m):
    """
    Extended Euclidean algorithm to find d = e^{-1} mod m.
    Returns old_s, which is the modular inverse of e (mod m),
    adjusted to be positive as in the spec.
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = m, e

    while r != 0:
        quotient = old_r // r  # truncated division
        # (old_r, r) <- (r, old_r - quotient*r)
        temp = r
        r = old_r - quotient * r
        old_r = temp

        # (old_s, s) <- (s, old_s - quotient*s)
        temp = s
        s = old_s - quotient * s
        old_s = temp

        # (old_t, t) <- (t, old_t - quotient*t)
        temp = t
        t = old_t - quotient * t
        old_t = temp

    if old_s < 0:
        old_s = old_s + m
    return old_s  # this is d


# =======================
# RSA Key Setup
# =======================

# Choose 4-digit primes p and q such that
# n = p*q satisfies 90909090 < n < 9090909090

p = 9127
q = 9967

n = p * q
phi = (p - 1) * (q - 1)  # m in the problem statement

# Choose e relatively prime to phi
e = 17  # a small common choice; we verify gcd(e, phi) == 1

if gcd(e, phi) != 1:
    raise ValueError("e is not relatively prime to (p-1)(q-1); choose a different e")

# Compute d = inverse of e mod phi using extended_gcd
d = extended_gcd(e, phi)

print(f"p = {p}, q = {q}")
print(f"n = p*q = {n}")
print(f"phi = (p-1)(q-1) = {phi}")
print(f"Public key (n, e) = ({n}, {e})")
print(f"Private exponent d = {d}")
print(f"Check: (e*d) mod phi = {(e * d) % phi}")


# =======================
# Block Encoding / Decoding
# =======================

def text_to_blocks(text):
    """
    1. Convert text to uppercase.
    2. Remove spaces.
    3. Group into blocks of 4 letters, padding with 'X' if needed.
    4. Convert each 4-letter block into an 8-digit integer by
       concatenating each letter's ASCII code (2 digits each, 65-90).
    Returns a list of integers (M values).
    """
    # Step 1 & 2
    cleaned = ''.join(ch for ch in text.upper() if ch.isalpha())

    # Step 3: pad to a multiple of 4 with 'X'
    if len(cleaned) % 4 != 0:
        cleaned += 'X' * (4 - len(cleaned) % 4)

    blocks = []
    for i in range(0, len(cleaned), 4):
        block = cleaned[i:i+4]  # 4 characters
        # Step 4: encode to 8-digit integer
        digits = ''.join(f"{ord(c):02d}" for c in block)
        M = int(digits)
        blocks.append(M)
    return blocks


def blocks_to_text(blocks):
    """
    Convert a list of 8-digit integers back into 4-letter blocks, then to text.
    Assumes each integer corresponds to 4 ASCII codes, 2 digits each.
    Returns the full decoded text (without removing padding).
    """
    chars = []
    for M in blocks:
        # Ensure we have 8 digits including leading zeros
        digits = f"{M:08d}"
        for i in range(0, 8, 2):
            ascii_code = int(digits[i:i+2])
            chars.append(chr(ascii_code))
    return ''.join(chars)


# =======================
# Encryption / Decryption
# =======================

def encrypt_blocks(blocks, e, n):
    """Encrypt a list of plaintext block integers M to ciphertext block integers C."""
    encrypted = []
    for M in blocks:
        C = modular_pow(M, e, n)
        encrypted.append(C)
    return encrypted


def decrypt_blocks(blocks, d, n):
    """Decrypt a list of ciphertext block integers C to plaintext block integers M."""
    decrypted = []
    for C in blocks:
        M = modular_pow(C, d, n)
        decrypted.append(M)
    return decrypted


# =======================
# Main Logic
# =======================

plaintext = "The camera is hidden in the bushes"

# Convert plaintext to 4-letter blocks -> list of M values
M_blocks = text_to_blocks(plaintext)
print("\nPlaintext blocks (M):")
print(M_blocks)

# Encrypt each block
C_blocks = encrypt_blocks(M_blocks, e, n)
print("\nCiphertext blocks (C):")
print(C_blocks)

# Write encrypted blocks to a file (encrypt.rsa)
with open("encrypt.rsa", "w") as f:
    # One block per line for simplicity
    for C in C_blocks:
        f.write(str(C) + "\n")

# Read encrypted blocks from encrypt.rsa
read_C_blocks = []
with open("encrypt.rsa", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            read_C_blocks.append(int(line))

# Decrypt blocks
decrypted_M_blocks = decrypt_blocks(read_C_blocks, d, n)
print("\nDecrypted M blocks:")
print(decrypted_M_blocks)

# Convert decrypted M blocks back to text
decrypted_text_with_padding = blocks_to_text(decrypted_M_blocks)

# Remove any trailing 'X' that might have been padding
decrypted_text = decrypted_text_with_padding.rstrip('X')

print("\nDecrypted text (after removing padding X):")
print(decrypted_text)

# Write decrypted message to decrypt.rsa
with open("decrypt.rsa", "w") as f:
    f.write(decrypted_text + "\n")
