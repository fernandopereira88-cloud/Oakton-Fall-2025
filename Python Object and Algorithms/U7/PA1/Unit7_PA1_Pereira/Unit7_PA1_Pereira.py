'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/03/2025
############################################################################################################################
ASSIGNMENT: HuffMan Coding
================================================================================================================================================================================================================        
ASSIGNMENT: Write a program to implement file compression using Huffman’s Algorithm (see algorithm
below). The program must use the heap (binary tree) implementation of a priority queue
provided by your textbook’s source code.

ASSIGNMENT QUESTIONS:

Question: Compute the total number of bits of the encoded passage. [1 point]
Answer: the encoded message has 38 bits, so the ocmpression algorithm was able to save 1 bit (details in the application report)
    
Question: How many bits are required if it is not encoded? Each symbol requires a 3 bit code since there are 23 = 8 distinct symbols. [1 point]
Answer: the orinal message has 13 characters, so 13 * 3 means it takes 39 bits when not encoded (verified with application report)

Question: What is the redundancy (in bits) of the passage? Find this by computing 𝑇 − ⌈𝑇 𝐻⌉. 
Answer: 
The redundance for the passage is 0 because the total number of bits encoded (38) is the same as the ceiling of the theoretical lower bound (T_H).
This translates into the compression being efficient, despite it only saving 1 bit.

==== ANALYSIS REPORT (PRINTED FROM main())=================
| Char	| Freq	| Code	| Len	| Total Bits |
| E		| 1		| 000	| 3		| 3			 |
| A		| 2		| 111	| 3		| 6			 |
| C		| 2		| 100	| 3		| 6			 |
| H		| 2		| 110	| 3		| 6			 |
| T		| 3		| 01	| 2		| 6			 |
| O		| 1		| 1011	| 4		| 4			 |
| B		| 1		| 1010	| 4		| 4			 |
|  		| 1		| 001	| 3		| 3			 |

Total characters: 13
Total bits encoded: 38
Total bits (no encoding, using 3 bits per character): 39
Average length (L): 2.923077 bit/character
Entropy (H): 2.873141 bits/character
Theoretical lower bound T_H: 37.350829
ceil(T_H): 38
Redundancy (T - ceil(T_H)): 0

'''
from goodrich.ch09.heap_priority_queue import HeapPriorityQueue
import math

class HuffmanNode:
    
    def __init__(self,frequency,character=None,left=None,right=None):
        '''
        Description: Huffman Node constructor
        Inputs:
            - frequency: holds the number of times the characters is present
            - character: holds the character value for the node
            - left: Internal nodes only. Maps node to a left child. None by default. 
            - right: Internal nodes only. Maps node to a right child. None by default. 
        Outputs:
            - None
            
        '''
        self._frequency = frequency
        self._character = character # Internal nodes will have it as "None"
        self._left = left
        self._right = right
        
    def is_leaf(self):
        '''
        Description: evaluates whether the node is a leaf or not
        Input: 
            - None
        Output:
            - True if the node is a leaf, false otherwise         
        '''
        if self._left == None and self._right == None:
            return True
        else:
            return False
    
 
    
def build_huffman_tree(character_frequencies,tracing=0):
    '''
    Description:
        - Uses a minHeap to build a huffman tree in which internal nodes represent merged leafs, 
          and leaves hold the characters in the compressed message
    Inputs:
        - character_frequencies: a dictionary contraining characters as key and their respective frequencies as values
        - tracing: 0 by default. If 1, prints the constructions of the huffman tree step by step.
    Outputs:
        - A node that holds the huffman tree for compression
    
    '''
    min_heap = HeapPriorityQueue()
    
    for character,frequency in character_frequencies.items():
        character_node = HuffmanNode(character=character,frequency=frequency)
        min_heap.add(frequency,character_node)
    if tracing ==1:
        i = 1
        print("\nStep-by-step build of the Huffman Tree:")
    while len(min_heap) > 1:
        # Remove the least counts
        f1,T1 = min_heap.remove_min()
        f2,T2 = min_heap.remove_min()
        
        # Add them together
        # Control for merging alphabetically when encountering ties.
        if T1._character <= T2._character:        
            added_frequencies = f1+f2
            concat_characters = T1._character + T2._character
        else:
            added_frequencies = f2+f1
            concat_characters = T2._character + T1._character
            
        # Print suport for algorithm tracing
        if tracing ==1:
            print(f"Step {i}: {T1._character}({f1}) + {T2._character}({f2}) --> {concat_characters}({added_frequencies})")
        
        # Create a new binary tree with left  subtree T1, and right subtree T2
        T = HuffmanNode(frequency=added_frequencies, character=concat_characters,left = T1, right = T2)
        
        # Insert T into Q with key f1+f2
        min_heap.add(added_frequencies,T)
        if tracing ==1:        
            i += 1
    
    freq,T = min_heap.remove_min()
    
    return T
    
def compute_frequency(input_text):
    '''
    Description: creates a dictionary with characters as key and character count as values
    Input: a string that will be used to count character frequency
    Output: a dictionary with character frequency
    '''    
    freq = dict()
    for ch in input_text:
        freq[ch] = freq.get(ch,0) + 1
    return freq
        

def build_huffman_codes(huffman_node):
    '''
    Description:
        - Uses the information from a huffman tree to build a dictionary that maps characters to a custom binary code. 
          The custom binary code can assign fewer bits than usual to a character, allowing the original content to be compressed.    
    Inputs:
        - huffman_tree: a huffman tree to be used to create a binary code compression for a message
    Outputs:
        - huffman_codes: a dictionary with the characters that will be used in compression and their respective customized binary codes for compression
    '''
    huffman_codes = {}
    
    def dfs(node,prefix):
        '''
        Description: recursive function to perform the depth-first search (dfs) for the huffman tree
        Inputs:
            - node: the node being analyzed
            - prefix: the huffman (binary) code for the node (that is recursively adjusted)
        Outputs:
            - Adjusted codes in the huffman_codes dictionary
        '''
        # Base case = Reached a Leaf
        if node is None:
            return
        if node.is_leaf():
            huffman_codes[node._character] = prefix if prefix != "" else "0"
            return 
        
        # Recursion to generate huffman codes
        dfs(node._left, prefix + "0")
        dfs(node._right, prefix + "1")
    #Calls recursive function to generate huffman codes
    dfs(huffman_node,"")
    
    return huffman_codes

def encode_text(text,huffman_codes):
    '''
    Description:
        - Uses the original content to be compressed and the huffman_codes dictionary with custom binary digits to generate an encoded version of the original content.
    Inputs:
        - text: the original content to be compressed
        - huffman_codes: a dictionary containing the mapping of the characters in the original content to their custom binary code
    Outpus:
        - Returns a string with the encoded characters
    '''
    return "".join(huffman_codes[ch] for ch in text)
     
def compress_file(input_filename,output_filename):
    '''
    Description: Calls multiple functions to perform the Huffman coding compression algorithm
    Inputs:
        - input_filename: the filename (with its extension) that will be compressed.
        - output_filename: the filename (with its extension) that will store the compressed content.
    Outputs:
        - text: the original passage that was compressed (returned for check purposes)
        - frequency: a dictionary containing the mapping of characters in "text" and their respective count in "text"
        - huffman_codes: a dicionary mapping each character in "text" to a custom binary code for the compressing algorithm
        - encoded_bits: the compressed version of "text" in bits
    '''
    with open(input_filename,"r") as read_file:
        text = read_file.read()
    
    
    frequency = compute_frequency(text)
    
    sorted_frequency = sorted(frequency.items(), key = lambda item: item[1], reverse = True)
        
    huffman_node = build_huffman_tree(frequency)
    huffman_codes = build_huffman_codes(huffman_node)
    encoded_bits = encode_text(text,huffman_codes)
    
    with open(output_filename,"w") as write_file:
        # Number of distinct characters
        write_file.write(str(len(frequency))+"\n")
        
        # Character and Frequencies description table
        for ch,fr in frequency.items():
            write_file.write(f"{repr(ch)} {fr}\n")
            
        write_file.write("\n")    
        
        # Encoded
        write_file.write(encoded_bits)
        
    return text, frequency, huffman_codes, encoded_bits

def decode_bits(bits,tree):
    '''
    Description: decodes an encoded message using the huffman tree
    Inputs:
        - bits: holds a sequence of bits that holds the compressed content
        - tree: the huffman tree built from the character-bit mapping table
    Outputs:    
        - returns a string with the decoded content
    '''
    S = ""
    P = tree # Iterator
    n = len(bits)
    
    for index in range(n):
        if bits[index] == "0":
            P = P._left
        else:
            P = P._right
            
        if P.is_leaf():
            S = S + P._character
            P = tree
            
    return "".join(S)            

def decompress_file(input_filename):
    '''
    Description: Calls multiple functions to decode content compressed through the Huffman coding algorithm
    Inputs:
        - input_filename: the filename (with its extension) to be used for decompression
    Outputs:    
        - decoded_text: the decompressed content
    '''
    
    with open(input_filename,"r") as read_file:
        lines = read_file.read().splitlines()
        
    index = 0
    
    # Capture number of distinct symbol
    k = int(lines[index])
    index += 1
    
    # Create frequency table mapping
    
    frequencies = dict()
    for _ in range(k):
        line = lines[index]
        index += 1
        ch_repr,fr_string = line.rsplit(" ",1)
        ch_string = eval(ch_repr)
        fr = int(fr_string)
        frequencies[ch_string] = fr
    
    while index < len(lines) and lines[index] == "":
        index +=1
    
    # Get encoded message
    encoded_bits = "".join(lines[index:]) # Using join in case of multiple lines
    
    # Recreate tree for decoding
    huffman_tree = build_huffman_tree(frequencies)
    
    # Decode using the tree
    decoded_text = decode_bits(encoded_bits,huffman_tree)
    
    return decoded_text

def analyze_passage(text,frequency,codes,output_table_filename="table.out"):
    '''
    Description: 
        - Performs the requested analysis for the content taken through the Huffman coding algorithm. Analysis:
            - A table containing a summary of Character, Frequency, Custom Binary Code, Length, and Total Bits
            - Total characters, encoded bits, and not encoded bits
            - Entropy, theoretical lower bound, and redundancy
    
    Inputs:
        - text:
        - frequency:
        - codes:
        - output_table_filename: the filename (with its extension) in which the analysis results are stored
    Outputs:    
        - A file with the analysis
        - A console print with the analysis report
    '''        
    n = len(text)
    bits_unencoded = n*3
    H = 0.0 # Entropy (H)
    T = 0
    for ch, fr in frequency.items():
        # Avg length
        T += fr * len(codes[ch])
        # Entropy
        p = fr / n
        H += -p * math.log2(p)
            
    L = T / n # Average length
        
    # Redundancy    
    T_H = H*n    
    ceil_T_H = math.ceil(T_H)    
    redundancy = T - ceil_T_H
    
    # Write table
    with open(output_table_filename, "w") as write_file:
        write_file.write("| Char\t| Freq\t| Code\t| Len\t| Total Bits |\n")
        for ch, fr in frequency.items():
            code = codes[ch]
            length = len(code)
            total_bits = fr * length                                    
            write_file.write(f"| {ch}\t\t| {fr}\t\t| {code}\t| {length}\t\t| {total_bits}\t\t\t |\n")
        
        write_file.write("\n")
        write_file.write(f"Total characters: {n}\n")
        write_file.write(f"Total bits encoded: {T}\n")
        write_file.write(f"Total bits (no encoding, using 3 bits per character): {bits_unencoded}\n")
        write_file.write(f"Average length (L): {L:.6f} bit/character\n")
        write_file.write(f"Entropy (H): {H:.6f} bits/character\n")
        write_file.write(f"Theoretical lower bound T_H: {T_H:.6f}\n")
        write_file.write(f"ceil(T_H): {ceil_T_H}\n")
        write_file.write(f"Redundancy (T - ceil(T_H)): {redundancy}")

    # Print report
    print("========================")
    print("= COMPRESSION ANALYSIS =")
    print("========================")
    print("Passage:\n",text)
    print(f"\nTotal characters: {n}")
    print(f"Total bits encoded: {T}")
    print(f"Total bits (no encoding, using 3 bits per character): {bits_unencoded}")
    print(f"Average length (L): {L:.6f} bit/character")
    print(f"Entropy (H): {H:.6f} bits/character")
    print(f"Theoretical lower bound T_H: {T_H:.6f}")
    print(f"ceil(T_H): {ceil_T_H}")
    print(f"Redundancy (T - ceil(T_H)): {redundancy}")        

def main():
    '''
    Description: Main driver function working thorugh assignment question
    Inputs: huffman.in
    Output: 
        - huffman.out
        - table.out
        - Algorithm tracing report
        - Decompression checks
        - Passage analysis
    '''
    # Use your program to compress the provided input file (huffman.in). [10 points]
    # Your program should write the results to an output file (huffman.out). [5 points]
    print("======================================")
    print("= FILE COMPRESSION AND DECOMPRESSION =")
    print("======================================")
    original_text, frequency, huffman_codes, encoded_bits = compress_file(input_filename="huffman.in",output_filename="huffman.out")

    # Your program will then decompress (see algorithm below) the output file (huffman.out) and confirm the results match the original input file (huffman.in). [10 points]
    decoded_text = decompress_file(input_filename="huffman.out")
    if decoded_text == original_text:        
        print(f"Decompression succesfull! Output file has been decoded to the same original text")
        print(f"Original text: {original_text}")
        print(f"Decoded text: {decoded_text}")
    else:
        print("ISSUE: Decoded text does NOT match the original")
        
    
    # Implement Huffman’s Algorithm (pseudocode provided below) by manually tracing through the
    # steps used to build a Huffman coding tree (see Huffman Algorithm Trace document) on the
    # following passage: CHATBOT CHEAT
    passage = "CHATBOT CHEAT"
    
    # Algorithm Tracing Support #
    print("\n===========================")
    print("= HUFFMAN ALGORITHM TRACE =")
    print("===========================") 
    print(f"Passage: {passage}")   
    print("\nCharacter Frequencies:")
    print("Char\t| Count |")
    frequency = compute_frequency(passage)
    
    sorted_frequency = sorted(frequency.items(), key = lambda item: item[1], reverse = True)
    for k,v in sorted_frequency:
        print(f"{k}\t| {v}\t|")
        
    huffman_node = build_huffman_tree(frequency,tracing=1)
    huffman_codes = build_huffman_codes(huffman_node)
    encoded_passage = encode_text(passage,huffman_codes)
    decoded_passage = decode_bits(encoded_passage,huffman_node)
    print(f"Decoding check for {passage}: {passage == decoded_passage}")
    
    print()
    
    # Use your program to confirm the results of the coding tree. Additionally, the program should
    # generate a table labeling each symbol with its associated encoding, frequency, and total bits, and
    # give the total frequency and bits sum as output to the console or separate output file (table.out).
    # See an example of a similar table below (Table 1). [10 points]        
    
    # Compute the total number of bits of the encoded passage. [1 point]
    
    # How many bits are required if it is not encoded? Each symbol requires a 3 bit code since there
    # are 23 = 8 distinct symbols. [1 point]
    
    analyze_passage(passage,frequency,huffman_codes)
    
if __name__ == "__main__":
    main()