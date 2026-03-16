# huffman.py
#
# Huffman Coding using the textbook's HeapPriorityQueue
# CSC 255 - Unit 7 Programming Assignment

from collections import Counter
import math

# If these modules are in the same directory, use:
from goodrich.ch09.heap_priority_queue import HeapPriorityQueue


# =========================
# Huffman Tree Structures
# =========================

class HuffmanNode:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq      # frequency of this subtree
        self.char = char      # character for leaf nodes; None for internal nodes
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None


# =========================
# Core Huffman Algorithm
# =========================

def build_frequency(text):
    """
    Compute frequency f(c) of each character c in X.
    Returns a dict: char -> frequency.
    """
    return Counter(text)


def build_huffman_tree(freqs):
    """
    Implements Huffman(X) using the textbook heap-based priority queue.

    freqs: dict {char: frequency}
    Returns: root node of Huffman tree.
    """
    Q = HeapPriorityQueue()

    # for each character c in X do:
    #   Create single-node tree T storing c.
    #   Insert T into Q with key f(c).
    for c, f in freqs.items():
        node = HuffmanNode(freq=f, char=c)
        Q.add(f, node)

    # Edge case: if there is only one distinct symbol,
    # we still want a non-trivial tree (so code is not empty).
    if len(Q) == 1:
        f, only_node = Q.remove_min()
        dummy = HuffmanNode(freq=0, char=None)
        parent = HuffmanNode(freq=f, left=only_node, right=dummy)
        Q.add(parent.freq, parent)

    # while length(Q) > 1 do:
    while len(Q) > 1:
        # (f1, T1) = Q.remove_min()
        f1, T1 = Q.remove_min()
        # (f2, T2) = Q.remove_min()
        f2, T2 = Q.remove_min()

        # Create a new binary tree T with left subtree T1 and right subtree T2.
        merged_freq = f1 + f2
        T = HuffmanNode(freq=merged_freq, left=T1, right=T2)

        # Insert T into Q with key f1 + f2.
        Q.add(merged_freq, T)

    # (f, T) = Q.remove_min()
    f, T = Q.remove_min()
    return T


def build_codes(root):
    """
    Traverse the Huffman tree to build a dict: char -> code string of '0'/'1'.
    """
    codes = {}

    def dfs(node, prefix):
        if node is None:
            return
        if node.is_leaf():
            # If only one unique symbol, ensure code is not empty.
            codes[node.char] = prefix if prefix != "" else "0"
            return
        dfs(node.left, prefix + "0")
        dfs(node.right, prefix + "1")

    dfs(root, "")
    return codes


# =========================
# Encoding / Decoding
# =========================

def encode_text(text, codes):
    """
    Encode the text using the codes dict (char -> bitstring).
    Returns the concatenated string of '0'/'1'.
    """
    return "".join(codes[ch] for ch in text)


def decode_bits(bits, root):
    """
    Decompression Algorithm (decode(E)) from the assignment.

    Input: E as string of '0'/'1', and the Huffman tree root.
    Output: decoded original string X.
    """
    S = []
    P = root  # iterator to the root

    for b in bits:
        # if E[i] is '0' then P = P.left else P = P.right
        if b == '0':
            P = P.left
        else:
            P = P.right

        # if P.left and P.right are Empty then:
        if P.is_leaf():
            # S += P.symbol
            S.append(P.char)
            # Reinitialize P to the root of the binary encoding tree.
            P = root

    return "".join(S)


# =========================
# File I/O for compression
# =========================

def compress_file(input_filename, output_filename):
    """
    Compresses input_filename using Huffman coding and writes result to output_filename.

    File format (text-based):
      <number of distinct symbols>
      <repr(symbol)> <frequency>
      ...
      <blank line>
      <encoded bitstring 0/1...>

    Returns:
      (original_text, freqs, codes, encoded_bits)
    """
    with open(input_filename, "r", encoding="utf-8") as f:
        text = f.read()

    if len(text) == 0:
        raise ValueError("Input file is empty; Huffman coding is undefined.")

    freqs = build_frequency(text)
    root = build_huffman_tree(freqs)
    codes = build_codes(root)
    encoded_bits = encode_text(text, codes)

    with open(output_filename, "w", encoding="utf-8") as f:
        # number of distinct symbols
        f.write(str(len(freqs)) + "\n")
        # each line: repr(symbol) frequency
        for ch, fr in freqs.items():
            f.write(f"{repr(ch)} {fr}\n")
        f.write("\n")  # blank line
        f.write(encoded_bits)

    return text, freqs, codes, encoded_bits


def decompress_file(output_filename):
    """
    Reads the Huffman-compressed file written by compress_file,
    reconstructs the tree, and returns the decoded text.
    """
    with open(output_filename, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    if not lines:
        raise ValueError("Compressed file is empty or invalid.")

    idx = 0

    # First line: number of distinct symbols
    k = int(lines[idx].strip())
    idx += 1

    freqs = {}
    for _ in range(k):
        line = lines[idx].strip()
        idx += 1
        # line: "<repr(ch)> <freq>", e.g. "'A' 3"
        repr_part, freq_part = line.rsplit(" ", 1)
        ch = eval(repr_part)          # controlled input from repr()
        freq = int(freq_part)
        freqs[ch] = freq

    # Skip blank line(s)
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1

    # Remaining lines: encoded bitstring (could technically be multiple lines)
    encoded_bits = "".join(lines[idx:])

    # Rebuild tree and decode
    root = build_huffman_tree(freqs)
    decoded_text = decode_bits(encoded_bits, root)
    return decoded_text


# =========================
# Analysis for "CHATBOT CHEAT"
# =========================

def analyze_passage(text, freqs, codes, table_filename="table.out"):
    """
    Generates a table for the given passage:

      Symbol | Freq | Code | Len | TotalBits

    and computes:
      - total bits encoded T
      - total bits if not encoded (3 bits per symbol, because 2^3 = 8 symbols)
      - average length L (bits/symbol)
      - entropy H
      - T_H = H * n, ceil(T_H)
      - redundancy R = T - ceil(T_H)

    Writes the table to table_filename and prints a summary.
    """
    n = len(text)

    # Total bits of the encoded passage T
    T = 0
    for ch, fr in freqs.items():
        T += fr * len(codes[ch])

    # Not encoded: each symbol uses 3 bits
    bits_unencoded = n * 3

    # Average length L
    L = T / n

    # Entropy H
    H = 0.0
    for ch, fr in freqs.items():
        p = fr / n
        H += -p * math.log2(p)
    T_H = H * n
    ceil_T_H = math.ceil(T_H)

    # Redundancy R in "total bits" form they ask for: T - ceil(T_H)
    redundancy = T - ceil_T_H

    # Write the table
    with open(table_filename, "w", encoding="utf-8") as f:
        f.write("Symbol\tFreq\tCode\tLen\tTotalBits\n")
        for ch, fr in freqs.items():
            code = codes[ch]
            length = len(code)
            total_bits = fr * length

            if ch == " ":
                display = "<space>"
            elif ch == "\n":
                display = "<newline>"
            else:
                display = ch

            f.write(f"{display}\t\t{fr}\t\t{code}\t{length}\t{total_bits}\n")

        f.write("\n")
        f.write(f"Total symbols n = {n}\n")
        f.write(f"Total bits encoded T = {T}\n")
        f.write(f"Total bits (no encoding, 3 bits/symbol) = {bits_unencoded}\n")
        f.write(f"Average length L = {L:.6f} bits/symbol\n")
        f.write(f"Entropy H = {H:.6f} bits/symbol\n")
        f.write(f"Theoretical lower bound T_H = {T_H:.6f}\n")
        f.write(f"ceil(T_H) = {ceil_T_H}\n")
        f.write(f"Redundancy R = T - ceil(T_H) = {redundancy}\n")

    # Also print to console
    print("=== 'CHATBOT CHEAT' Analysis ===")
    print(f"n (total symbols) = {n}")
    print(f"Total bits encoded T = {T}")
    print(f"Total bits (no encoding, 3 bits/symbol) = {bits_unencoded}")
    print(f"Average length L = {L:.6f} bits/symbol")
    print(f"Entropy H = {H:.6f} bits/symbol")
    print(f"T_H = {T_H:.6f}, ceil(T_H) = {ceil_T_H}")
    print(f"Redundancy (T - ceil(T_H)) = {redundancy}")


# =========================
# Main Execution
# =========================

def main():
    # 1. Compress huffman.in -> huffman.out
    original_text, freqs, codes, encoded_bits = compress_file("huffman.in", "huffman.out")
    print("Compression complete. Output written to huffman.out")

    # 2. Decompress huffman.out and confirm equality with original
    decoded_text = decompress_file("huffman.out")
    if decoded_text == original_text:
        print("Decompression successful: decoded text matches original (huffman.in).")
    else:
        print("ERROR: decoded text does NOT match original!")

    # 3. Analyze the specific passage "CHATBOT CHEAT"
    passage = "CHATBOT CHEAT"
    passage_freqs = build_frequency(passage)
    passage_root = build_huffman_tree(passage_freqs)
    passage_codes = build_codes(passage_root)
    passage_encoded = encode_text(passage, passage_codes)

    # Optional sanity check: decoding the passage
    passage_decoded = decode_bits(passage_encoded, passage_root)
    print(f"Passage decoding check (CHATBOT CHEAT): {passage_decoded == passage}")

    # Generate table and stats for this passage
    analyze_passage(passage, passage_freqs, passage_codes, table_filename="table.out")
    print("Table and statistics for 'CHATBOT CHEAT' written to table.out")


if __name__ == "__main__":
    main()
