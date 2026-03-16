'''
############################################################################################################################
STUDENT: FERNANDO CHIAVERINI ALBANO PEREIRA
DATE: 12/05/2025
############################################################################################################################
ASSIGNMENT: 8-Queens
================================================================================================================================================================================================================        
Consider the problem of placing eight queens on an (eight-by-eight) chess board. Two queens
are said to attack each other if they are on the same row, column, or (not necessarily main)
diagonal.

ASSIGNMENT QUESTIONS:
QUESTION: Give a randomized algorithm to place eight non-attacking queens on the board. [20 points]

QUESTION: Give a backtracking algorithm to solve the same problem. [20 points]

QUESTION: Implement both algorithms and write a report comparing the running times. [10 points]

'''

import random
import time

# Randomized implementation
def is_safe(board):
    '''
    Docstring for is_safe
    
    :param board: Description
    '''
    n = len(board)
    main_diagonals = set()
    anti_diagonals = set()
    
    for col in range(n):
        row = board[col]
        d1 = row - col
        d2 = row + col
        if d1 in main_diagonals or d2 in anti_diagonals:
            return False
        main_diagonals.add(d1)
        anti_diagonals.add(d2)
    return True

def randomized_eight_queens():
    n = 8
    rows = list(range(n))
    
    attempts = 0
    
    while True:
        attempts += 1
        random.shuffle(rows)
        if is_safe(rows):
            return rows[:], attempts
        
        
# Backtracking implementation
def is_safe_partial(board,col,row):
    '''
    Docstring for is_safe_partial
    
    :param board: Description
    :param col: Description
    :param row: Description
    '''
    for c_prev in range(col):
        r_prev = board[c_prev]
        if r_prev == row:
            return False
        if r_prev - c_prev == row - col:
            return False
        if r_prev + c_prev == row + col:
            return False
        
    return True

def backtrack(board, col):
    n = len(board)
    if col == n:
        return True
    
    for row in range(n):
        if is_safe_partial(board,col,row):
            board[col] = row
            if backtrack(board, col +1):
                return True
            board[col] = -1
    return False

def backtracking_eight_queens():
    '''
    Docstring for backtracking_eight_queens
    '''
    n = 8
    board = [-1] * n
    success = backtrack(board, 0)
    return board if success else None

# Timing algorithms
def time_randomized(trials=1000):
    '''
    Docstring for time_randomized
    
    :param trials: Description
    '''
    start = time.time()
    total_attempts = 0    
    for _ in range(trials):
        _, attempts = randomized_eight_queens()
        total_attempts += attempts
    end = time.time()
    
    avg_time = (end - start) / trials
    avg_attempts = total_attempts / trials
    
    return avg_time, avg_attempts

def time_backtracking(trials=1000):
    '''
    Docstring for time_backtracking
    
    :param trials: Description
    '''
    start = time.time()    
    for _ in range(trials):
        backtracking_eight_queens()
    end = time.time()
    avg_time = (end - start)/trials
    return avg_time


def main():
    '''
    Docstring for main
    '''
    randomized_time,randomized_attempts = time_randomized()
    backtracking_time = time_backtracking()
    
    print(f"\nRandomized algorithm: avg time = {randomized_time:.8f}s, avg attempts {randomized_attempts:.8f}")
    print(f"Backtracking algorithm: avg time = {backtracking_time:.8f}s")
    
if __name__ == "__main__":
    main()
    