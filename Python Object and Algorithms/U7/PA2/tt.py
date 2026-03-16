import random
import time

N = 8

# =========================
#  Backtracking Algorithm
# =========================

def is_safe_backtracking(board, row, col):
    # Check row on left side
    for c in range(col):
        if board[row][c] == 1:
            return False

    # Check column above
    for r in range(row):
        if board[r][col] == 1:
            return False

    # Check upper-left diagonal
    r, c = row - 1, col - 1
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            return False
        r -= 1
        c -= 1

    # Check lower-left diagonal
    r, c = row + 1, col - 1
    while r < N and c >= 0:
        if board[r][c] == 1:
            return False
        r += 1
        c -= 1

    # Check upper-right diagonal
    r, c = row - 1, col + 1
    while r >= 0 and c < N:
        if board[r][c] == 1:
            return False
        r -= 1
        c += 1

    # Check lower-right diagonal
    r, c = row + 1, col + 1
    while r < N and c < N:
        if board[r][c] == 1:
            return False
        r += 1
        c += 1

    return True


def solve_8_queens(board, col, stats):
    """
    Backtracking solver following the given pseudocode.
    stats["retries"] counts how many placements are later undone (backtracks).
    """
    if col == N:
        return True  # All queens placed successfully

    for row in range(N):
        if is_safe_backtracking(board, row, col):
            board[row][col] = 1  # Place queen

            if solve_8_queens(board, col + 1, stats):
                return True

            # Backtrack: remove queen
            board[row][col] = 0
            stats["retries"] += 1  # count this as a retry

    return False  # No safe position in this column


def backtracking_eight_queens():
    board = [[0 for _ in range(N)] for _ in range(N)]
    stats = {"retries": 0}
    start = time.time()
    success = solve_8_queens(board, 0, stats)
    end = time.time()
    if not success:
        return None, stats["retries"], end - start
    return board, stats["retries"], end - start


# =========================
#  Randomized Algorithm
# =========================

def is_safe_randomized(permutation):
    """
    permutation[c] = row of queen in column c
    Check that no two queens share a diagonal.
    """
    main_diagonals = set()
    anti_diagonals = set()

    for col in range(N):
        row = permutation[col]
        d1 = row - col
        d2 = row + col
        if d1 in main_diagonals or d2 in anti_diagonals:
            return False
        main_diagonals.add(d1)
        anti_diagonals.add(d2)

    return True


def randomized_eight_queens():
    """
    Randomized algorithm:
    - Generate random permutations of rows until we find a safe one.
    - Count how many permutations we tried.
    """
    rows = list(range(N))
    attempts = 0
    start = time.time()

    while True:
        attempts += 1
        random.shuffle(rows)
        if is_safe_randomized(rows):
            end = time.time()
            # Build a 2D board representation just like the backtracking one
            board = [[0 for _ in range(N)] for _ in range(N)]
            for col in range(N):
                row = rows[col]
                board[row][col] = 1
            return board, attempts, end - start


# =========================
#  Utility
# =========================

def print_board(board):
    for r in range(N):
        line = ""
        for c in range(N):
            line += "Q " if board[r][c] == 1 else ". "
        print(line)
    print()


# =========================
#  Timing & Comparison
# =========================

def compare_algorithms(trials=100):
    # Randomized
    total_rand_time = 0.0
    total_rand_attempts = 0

    for _ in range(trials):
        _, attempts, elapsed = randomized_eight_queens()
        total_rand_time += elapsed
        total_rand_attempts += attempts

    avg_rand_time = total_rand_time / trials
    avg_rand_attempts = total_rand_attempts / trials

    # Backtracking
    total_back_time = 0.0
    total_back_retries = 0

    for _ in range(trials):
        _, retries, elapsed = backtracking_eight_queens()
        total_back_time += elapsed
        total_back_retries += retries

    avg_back_time = total_back_time / trials
    avg_back_retries = total_back_retries / trials

    print(f"=== Comparison over {trials} trials ===")
    print("Randomized algorithm:")
    print(f"  Average time      : {avg_rand_time:.8f} seconds")
    print(f"  Average attempts  : {avg_rand_attempts:.2f} permutations")
    print()
    print("Backtracking algorithm:")
    print(f"  Average time      : {avg_back_time:.8f} seconds")
    print(f"  Average retries   : {avg_back_retries:.2f} backtracks")


if __name__ == "__main__":
    # Run each algorithm once and show a sample solution
    print("Randomized 8-Queens (single run):")
    rand_board, rand_attempts, rand_time = randomized_eight_queens()
    print_board(rand_board)
    print(f"Randomized attempts: {rand_attempts}")
    print(f"Randomized time    : {rand_time:.8f} seconds\n")

    print("Backtracking 8-Queens (single run):")
    back_board, back_retries, back_time = backtracking_eight_queens()
    print_board(back_board)
    print(f"Backtracking retries: {back_retries}")
    print(f"Backtracking time   : {back_time:.8f} seconds\n")

    # Compare average performance
    compare_algorithms(trials=100)
