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
ANSWER:
    - Represent the board using a list with 8 elements. The matrix indices represent the board column [0 to 7], and the values represent the rows (also restricted between 0 and 7, inclusive)
    - The list is shuffled to randomize the placement of the queens in different rows. However, given the list set up, each queen will be in a different row and colummn.
    - If the queens have their diagonals safe, the board meets the 8-queens problem (because rows and columns where unique at set up)
    - If there are conflicts, shuffle the board for another solution.This approach implies that a random number of attempts will be required to find a solution each time. This number is likely to be different each time.
    - Pseudocode:
        FUNCTION randomized_queens():
            rows = [0,1,2,3,4,5,6,7]
            repeat:
                shuffle(rows)
                IF is_safe(rows) is TRUE, RETURN rows and complete the algorithm
                
        FUNCTION is_safe(rows):
            n received the board length
            main_diagonals is an empty set
            secondary_diagonals is an empty set
            
            for cols 0 to n:
                row = board[col]
                d1 = row - col
                d2 = row + col
                IF d1 in main_diagonals OR d2 in secondary_diagonals:
                    return False
                add d1 to main_diagonals
                add d2 to secondary_diagonals
            return True
                
QUESTION: Give a backtracking algorithm to solve the same problem. [20 points]
ANSWER:
    - The backtracking algorithm will try to solve the 8-queens problem by placing a queen in each column, one by one. 
    If the placemenet is safe, the algorithm moves to the next column, else go back to the previous column and try a different position.
    - The backtracking will be implemented recursively.

    - Pseudocode:
    FUNCTION solve_8_queens(board,col) --> board: a lists of lists that represents a chess board / col: the column on the board being evaluated for a queen placement
        Check IF col is the last column, if "Yes" RETURN TRUE as all queens were placed succesfuly
        
        FOR each row on the board
            IF is_safe(board, row, col)
                Place queen in row,col
                IF solve_8_queens(board,col +1) 
                    RETURN True
                ELSE Backtrack and Remove queen
        RETURN False as no safe positiion was found in the column
    
    FUNCTION is_safe(board,row,col)
        Check IF queen is safe in row, column, and diagonals                


QUESTION: Implement both algorithms and write a report comparing the running times. [10 points]
ANSWER: 
In general, the randomized algorithm required more than twice the time of the backtracking algorithm (Randomized Avg time: 0.0006 vs Backtracking Avg time: 0.0003)
While the backtracking algorithm is capable of solving the problem with 105 retries, the randomized has to reshuffle the board, on average, 444 times.

RUNTIME REPORT:
=========================================
= ALGORITHM COMPARISON FOR 1,000 TRIALS =
=========================================
RANDOMIZED   - Average Time: 0.000684s | Average Attempts:      444
BACKTRACKING - Average Time: 0.000333s | Average Retries:       105

'''

import random
import time

# Randomized implementation
def is_safe_randomized(permutation,n=8):
    '''
    Description: a boolean function that analyzes the main and secondary diagonals of the shuffled board, evaluating whether queens are safe on those
    Inputs:
        - permutation: a shuffled list in which indexes represent the columns in which queens are placed, and values represent their rows.
        - n: the board size. Set to 8 by default.
    Outputs:
        - Boolean (True/False): True when diagonals are safe, False otherwise.
    
    :param board: Description
    '''
    main_diagonals = set()
    secondary_diagonals = set()
    
    for col in range(n):
        row = permutation[col]
        d1 = row - col # two queens in the same main diagonal will have the same row - col value
        d2 = row + col # two queens in the same secondary diagonal will have the same row + col value
        if d1 in main_diagonals or d2 in secondary_diagonals:
            return False
        main_diagonals.add(d1)
        secondary_diagonals.add(d2)
    return True

def randomized_queens(n = 8):
    '''
    Description:
        - Main function for the randomized queens algorithm. It initializes the board, times the algorith, shuffles the board, and returns a solution when it is found.
    Inputs:
        - n: the size of the board
    Outputs:
        - board: a lists of lists that represents a chess board (8x8) with the placed queens
        - attempts: the number of times the board had to be reshuffles until a solution was found
        - end - start: the duration of the algorithm in seconds
    '''
    
    rows = list(range(n))
    attempts = 0
    start = time.time()
    
    while True:
        attempts += 1
        random.shuffle(rows)
        if is_safe_randomized(rows):
            end = time.time()
            board = [[0 for _ in range(n)] for _ in range(n)]
            for col in range(n):
               row = rows[col]
               board[row][col] = 1 
            return board, attempts, end - start
        
        
# Backtracking implementation
def is_safe_backtracking(board,col,row):
    '''
    Description: a boolean function that evaluates the queen safety form other queens already in the board.
    Inputs:
        - board: Description
        - col: Description
        - row: Description
    Outputs:
        - Evaluates True when the queen is safe from other queens already on the board, and False otherwise
    '''
    # Check the Row on the left-side
    for c in range(col):
        if board[row][c] == 1:
            return False
        
    # Check the Column above
    for r in range(row):
        if board[r][col] == 1:
            return False
        
    # Check upper-left diagonal
    r,c = row-1, col-1
    while r>=0 and c>= 0:
        if board[r][c] == 1:
            return False
        r -= 1
        c -= 1
    
    # Check lower-left diagonal
    r, c = row + 1, col -1
    while r < len(board) and c>= 0:
        if board[r][c] == 1:
            return False
        r += 1
        c -= 1
        
    # Check upper-right diagonal
    r, c = row -1 , col + 1
    while r >= 0 and c < len(board):
        if board[r][c] == 1:
            return False
        r -= 1
        c += 1
    
    # Check lower-right diagonal
    r, c = row + 1, col + 1
    while r < len(board) and c < len(board):
        if board[r][c] == 1:
            return False
        r += 1
        c += 1
        
    return True

def solve_queens_backtracking(board, col,stats):
    '''
    Description: performs the backtracking part of the algorithm, looping each placement to check for queen safety, and using recursion to place all the queens accordingly
    Inputs:
        - board: a lists of lists representing the chess board
        - col: the column the be evaluated for placement
        - stats: a dictionary used to calculate the number of retries the algorithm needed
    Outputs: 
        - Boolean (True/False): True when a solution in found, and False when queens are not safe.
    '''
    n = len(board)
    if col == n:
        return True
    
    for row in range(n):
        if is_safe_backtracking(board,col,row):
            board[row][col] = 1 # Place queen
            if solve_queens_backtracking(board, col +1,stats):
                return True
            board[row][col] = 0
            
            stats['retries'] += 1
            
    return False

def backtracking_queens(n = 8):
    '''
    Description: Initializes and sets up the backtracking algorithm
    Inputs:
        - n: the number of rows and columns in the chess board. Set to 8 by default.
    Outputs:
        - board: a lists of lists that represents a chess board (8x8) with the placed queens
        - stats['retries]: the number of retries needed until reaching the solution
        - end - start: the duration of the algorithm in seconds
    '''
    
    board = [[0 for _ in range(n)] for _ in range(n)]
    stats = {'retries':0}
    start = time.time()
    success = solve_queens_backtracking(board, 0,stats)
    end = time.time()
    if not success:
        return None, stats['retries'], end - start
    else:
        return board, stats['retries'], end - start    
    
# Utilities / Helper functions

    # Printing board
def print_board(board):
    '''
    Description: Helper function to print the chess board and the placed queens
    Inputs: 
        - board: the chess board represented as a list of lists
    Outpus:
        - None passed to the user, but displays the board with Queens (Q) placed
    '''
    for r in range(len(board)):
        line = ""
        for c in range(len(board)):
            line += "Q " if board[r][c] == 1 else ". "
        print(line)
    print()
    
def compare_algorithms(trials):
    '''
    Descriptions: Helper function to compare runtime and attempts of algorithms over a number of trials
    
    Inputs:
        - trials: Description
    Outputs:
        - None passed back to the user, but displayes a report comparing runtime, and attempts vs retries for the Randomized and the Backtracking algorithms
    '''
    total_randomized_time = 0.0
    total_randomized_attempts = 0
    total_backtracking_time = 0.0
    total_backtracking_retries = 0
    
    for _ in range(trials):
        _, attempts, duration = randomized_queens()
        total_randomized_time += duration
        total_randomized_attempts += attempts
        
        _, retries, duration = backtracking_queens()
        total_backtracking_time += duration
        total_backtracking_retries += retries
        
    avg_randomized_time = total_randomized_time/trials
    avg_randomized_attempts = total_randomized_attempts/trials
    
    avg_backtracking_time = total_backtracking_time/trials
    avg_backtracking_retries = total_backtracking_retries/trials
    
    print("\n=========================================")
    print(f"= ALGORITHM COMPARISON FOR {trials:,.0f} TRIALS =")
    print("=========================================")
    print(f"RANDOMIZED   - Average Time: {avg_randomized_time:.6f}s | Average Attempts:\t{avg_randomized_attempts:.0f}")
    print(f"BACKTRACKING - Average Time: {avg_backtracking_time:.6f}s | Average Retries:\t{avg_backtracking_retries:.0f}")

    
def main():
    '''
    Description: driver function that calls one execution of each algorithm, simulates algorithms for runtime comparison, and reports the results to the user
    Inputs: 
        - None
    Outputs:
        - None passed to the user, but displays information about algorithms and results.
    '''

    print("\n=============================")
    print(f"= ALGORITHM EXECUTION CHECK =")
    print("=============================")    
    
    # Randomized
    randomized_board,randomized_attempts, randomized_duration = randomized_queens()
    print("\nFinal RANDOMIZED Board:")
    print_board(randomized_board)
    print(f"\nRetries: {randomized_attempts}, Runtime: {randomized_duration:.8}s")
    
    # Backtracking
    backtracking_board,backtracking_retries,backtracking_duration = backtracking_queens()
    print("\nFinal BACKTRACKING Board:")
    print_board(backtracking_board)
    print(f"\nRetries: {backtracking_retries}, Runtime: {backtracking_duration:.8}s")
    
    compare_algorithms(trials=1000)
    
if __name__ == "__main__":
    main()
    