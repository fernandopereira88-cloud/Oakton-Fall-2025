'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/07/2025
############################################################################################################################
ASSIGNMENT: RSA Encryption
================================================================================================================================================================================================================        
'''


def gcd(e,m):
    '''
    Description: Euclidean Algorithm. Used to verify the greatest common denominator (gcd) between two numbers and assert whether they are relatively prime.
    Inputs:
        - e: Factor 1 for the gcd algorithm
        - m: Factor 2 for the gcd algorithm
    Outputs:
        - x: The greatest common denominator between factors
    '''
    x = e 
    y = m
    while y != 0:
        r = x % y
        x = y
        y = r
    return x

def extended_gcd(e,m):
    '''
    Description: extended gcd algorithm to calculate the inverse of e
    Inputs:
        - e: Factor 1 for the gcd algorithm
        - m: Factor 2 for the gcd algorithm
    Outputs:
        - old_s: The result of extended gcd to be used as inverser of e for decription.
    '''
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = m
    old_r = e
    
    while r != 0:
        quotient = old_r // r
        temp = r
        r = old_r - quotient * r
        old_r = temp
        
        temp = s
        s = old_s - quotient * s
        old_s = temp
        
        temp = t 
        t = old_t - quotient*t
        old_t = temp
        
    if old_s < 0:
        old_s = old_s + m
        
    return old_s
    
    
def modular_pow(base,exponent,modulus):
    '''
    Description:
        - Calculates the modular exponentiation used both for encryption and decryption
        - Computes (base^exponent) mod modulus.
    Inputs:
    - base: an integer for the modular exponentiation
    - exponent: exponent for the modular exponentiation
    - modulus: modulus  for the modular exponentiation
    Outputs:
    - c: the result of the modular exponentiation
    '''
    if modulus == 1:
        return 0
    c = 1
    for e_prime in range(exponent):
        c = (c*base) % modulus
    return c
        
def encrypt(message: str, e: int, n:int):
    '''
    Description:
        - Encrypts a message considering pre-established RSA encrytpion algorithm parameters (e and n) passed by the user
    Inputs:
        - message: the message to be encrypted
        - e: public key parameter
        - n: the modulus for public and private keys
    Outputs:
        - cipher_blocks: a list with integers that represent encrypted block codes from the original message
    '''
    adjusted_message = message.upper().replace(" ","")
    
    message_digits_blocks = []
    
    for index in range(0,len(adjusted_message),4):
        block = adjusted_message[index:index+4]
        # If there are empty spaces at the end of a block, pad the end with the letter “X” (keep block size equalt 4)
        if len(block) < 4:
                block += "X"*(4-len(block))  
        # Convert ascii characters to digits using ord()                        
        digits_block = "".join(f"{ord(c):02d}" for c in block)
        message_digits_blocks.append(digits_block)        
     
    # Encryption
    cipher_blocks = []
    for item in message_digits_blocks:
        int_item = int(item)
        cipher = modular_pow(int_item,e,n) % n
        cipher_blocks.append(cipher)
    return cipher_blocks
    
def decrypt(encrypted_message_list: list[int], d: int, n: int):
    '''
    Description:
        - Decrypts the items provided in encrypted_message_list by applying modular exponentiation considering pre-established RSA parameters passed into the fucntion (d, and n)
    
    Inputs:
        - encrypted_message_list: a list with encrypted blocks to be decrypted
        - d: theoutput of the extended Euclidean algorithm that returns the inverse of e
        - n: the public part of the key (modulos)
    Outputs:
        - The decrypted message is returned back to the user without padding
    '''
    decrypted_blocks = []
    for block in encrypted_message_list:
        decrypted_block = modular_pow(block,d,n)
        decrypted_blocks.append(decrypted_block)
        
    # Convert back to ascii
    chars = []
    for block in decrypted_blocks:
        digits = f"{block:08d}" # Ensures 8 digits
        for i in range(0,8,2): # Maximum block length is 8 and Each character is 2 digits
            ascii_code = int(digits[i:i+2])
            chars.append(chr(ascii_code)) # transforms code back to char
    
    decrypted_message_padded = ''.join(chars)
            
    # Remove padding 
    decrypted_message = decrypted_message_padded.rstrip("X")
    
    return decrypted_message
    
    
def main():
    '''
    Description: 
        - Main function driver for th RSA encryption assignment.
        - It defines encrytpion constant parameters p, q, and e, and calls a function to encrypt a message, writes the encrypted message in a file, 
          then calls a function to decrypt the message in the file, and displays the decrypted message back to the user.
    '''
    ##################
    # RSA Key Set up #
    ##################
    p = 9127
    q = 9967
    n = p * q
    p_1_q_1 = (p-1)*(q-1)
    e = 31
    
    check_relative_prime = gcd(e,p_1_q_1)
    
    if check_relative_prime != 1:
        raise ValueError("e is not reltively prime to (p-1)*(q-1). Choose another e.")
    
    d = extended_gcd(e, p_1_q_1) # Inverse variable for decription 
    
    
    message = "The camera is hidden in the bushes"
    ##############################
    # Calling Encryption program #
    ##############################
    encrypted_blocks_message = encrypt(message=message,e=e,n=n)
    
    with open("encrypt.rsa","w") as writeFile:
        for block in encrypted_blocks_message:
            writeFile.write(str(block)+ "\n")

    ##############################
    # Calling Decryption program #
    ##############################
    read_encrypted_blocks = []
    with open("encrypt.rsa",'r') as readFile:
        for line in readFile:
            line = line.strip()
            if line:
                read_encrypted_blocks.append(int(line))    
    
    decrypted_message = decrypt(encrypted_message_list=read_encrypted_blocks,d=d,n=n)
    
    print("\nDecrypted Message:")
    print(decrypted_message)
    
    with open("decrypt.rsa",'w') as writeFile:
        writeFile.write(decrypted_message+"\n")
    
    
if __name__ == "__main__":
    main()
