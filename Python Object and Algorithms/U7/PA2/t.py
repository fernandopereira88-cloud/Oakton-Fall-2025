def calcQueens(size):
    board = [-1] * size
    return queens(board,0,size)

def queens(board,current,size):
    if (current == size):
        return True
    else:
        for i in range (size):
            board[current] = i
            if (noConflicts(board,current)):
                done = queens(board,current+1,size)
                if (done):
                    return True
        return False
    
def noConflicts(board,current):
    for i in range(current):
        if (board[i] == board[current]):
            return False
        if (current - i == abs(board[current] - board[i])):
            return False
    return True

print(calcQueens(size = 8))