#!/usr/bin/env python3
import sys
from copy import deepcopy
import random


# METHOD TO ROTATE THE BOARD
#First loop (0 to n) is applied to change columns while the internal loop ((n+3)-1 to 0) is
# iterating in reverse which is shifting each element down by 1.
# The last element at the end of the column is removed and is stored in removed_element.
# Once the elements are shifted by 1 we drop the removed element into the first column.
# Another loop (j=(n+3)-1 to 0) is iterating in reverse and checks the first empty position in the column
# starting from the bottom. At the first empty position the removed element is inserted.
def rotate(state, n):
    successor = []
    dropPiece = []
    for col in range(0, n):
        new_state = deepcopy(state)
        # SHIFTING EACH ELEMENT
        if new_state[(n + 3) - 1][col] != ".":
            removed_element = new_state[(n + 3) - 1][col]
            dropPiece.append(-(col + 1))
            new_state[(n + 3) - 1][col] = "."
            for i in range((n + 3) - 1, 0, -1):
                if new_state[i - 1][col] != ".":
                    new_state[i][col] = new_state[i - 1][col]
                    new_state[i - 1][col] = "."

            # DROPPING REMOVED PEBBLE
            for j in range((n + 3) - 1, 0, -1):
                flag = 0
                if new_state[j][col] == ".":
                    new_state[j][col] = removed_element
                    flag = 1
                    break
            if flag == 0:
                new_state[0][col] = removed_element

            successor.append(new_state)
    return dropPiece, successor


# METHOD TO DROP THE BOARD
# For every row from the bottom we check if there is any empty state.
#if so then we drop a piece into the particular column and then blacklist the cloumn.
#This step is scontinued until all possible drop moves are made 
def drop(state, n, turn):
    new_state = deepcopy(state)
    finalList = []
    addPiece = []
    for i in range(n + 2, -1, -1):
        for j in range(n - 1, -1, -1):
            if (state[i][j] == "." and j not in addPiece):
                new_state[i][j] = turn
                addPiece.append(j)
                finalList.append(new_state)
                new_state = deepcopy(state)
    addPiece = [x + 1 for x in addPiece]
    return addPiece, finalList


# SUCCESSOR RETURNS ALL THE SUCCESSORS OF THE CURRENT STATE
# This functions combines the output of rotate and drop into one and returns it the MINMAX
# A check is made to ensure that the number of pebbles for a particular palyer does 
# not increase n*(n+3)/2   
def successor(board, n, turn):
    succ_element = []
    succ = []
    move2 = []
    l2 = []
    move1, l1 = rotate(board, n)
    piece=sum(row.count(turn) for row in board)
    allowedPieces= n*(n+3)/2
    if(piece<allowedPieces):
        move2, l2 = drop(board, n, turn)
    for i in range(0, len(l1)):
        succ_element = [l1[i], move1[i]]
        succ.append(succ_element)
    for i in range(0, len(l2)):
        succ_element = [l2[i], move2[i]]
        succ.append(succ_element)

    return succ


# METHOD TO CHECK IF THE CURRENT STATE IS A GOAL STATE
# In this method we check if the nxn board is a goal state or not i.e. all rows, all columns and both the diagonals
# are checked for turn = x or o. The all() method of python is a standard library function which returns True when all
# elements in the given iterable are true. For checking all elements in column a temporary list lcol[] is taken which
# stores the elements of each column and then all() method is used to check if all elements are same in that list.
# Once this is done, the column is changed and the lcol[] is reset to empty by function del. The same procedure is applied for
# the diagonals except that the conditions are different for left (i==j) and right (i+j==n-1) diagonals.
def isGoal(n, board, turn):
    # CHECKING ALL ROWS
    i = 0
    for row in board:
        if all(element == turn for element in row) == True and i < n:
            return True
        i += 1

    # CHECKING ALL COLUMNS
    lcol = []
    for i in range(0, n):
        del lcol[:]
        for j in range(0, n):
            lcol.append(board[j][i])
        if all(element == turn for element in lcol) == True:
            return True

    # CHECKING ALL DIAGONALS
    leftdiag = []
    rightdiag = []
    for i in range(0, n):
        for j in range(0, n):
            leftdiag.append(board[i][j]) if i == j else False
            rightdiag.append(board[i][j]) if i + j == n - 1 else False
    if all(element == turn for element in leftdiag) == True:
        return True
    if all(element == turn for element in rightdiag) == True:
        return True

# HEURISTIC FUNCTION
#WE CHECK THE CURRENT STATE OF THE BOARD AND BASED ON THE PLAYER'S TURN WE ARE ASSIGNING MAX VALUE OF +100 FOR THE
# NUMBER OF PIECES THE MAX PLAYER HAS ON EVERY ROW, COLUMN AND DIAGONALS WHILE -50 FOR EVERY OPPONENT'S PIECE. WE RETURN THE MAX
# OF ALL THE SUMS AS THE HEURISTIC IF IT IS MAX'S TURN AND NEGATIVE OF THE MAX IF IT IS MIN'S TURN
def heuristic(board, n, turn, maxi,move):
    other = ""
    if turn == "x":
        other = "o"
    else:
        other = "x"
    row_count = []
    countdl = 0
    countdr = 0

    for row in range(0, n):
        countr = 0
        countc = 0
        c=0
        for col in range(0, n):
            if board[row][col] == turn:
                countr += 120
            elif board[row][col] == other:
                countr -= 50
            if board[col][row] == turn:
                countc += 120
                c+=1
            elif board[col][row] == other:
                countc -= 50
                c+=1
            if row == col and board[row][col] == turn:
                countdl += 120
            elif row == col and board[row][col] == other:
                countdl -= 50
            if row + col == n - 1 and board[row][col] == turn:
                countdr += 120
            elif row + col == n - 1 and board[row][col] == other:
                countdr -= 50
                
        if((row+1==move or row+1==-move)and c==n):        
         if(board[n+2][row]==turn):
             countc += 120
         else :
             countc -= 50
        row_count.append(countr)
        row_count.append(countc)
    row_count.append(countdl)
    row_count.append(countdr)
    if (maxi):
        return -max(row_count), turn, board
    else:
        return max(row_count), turn, board


# MINIMAX ALGORITHM
# here we have implemented the minmaxalgorithm with alpha-Beta pruning  
# we are passing "maximixing" as true in the begining(for max player)
# for min player we are passing "maximixing" as false.
# the depth keeps decresing by 1, we calculate the heuristic for depth=0 or when the goal state is reached
# the heurestic is stored in an eval variable, the maximizing player stores the max of eval while 
#the minimzing player stores the min of eval        
# used this site for reference of min max https://www.youtube.com/watch?v=l-hh51ncgDI    
        
def minimax(state, n, depth, alpha, beta, player, maximixing,moves):
    if player == "x":
        other = "o"
    else:
        other = "x"

    if isGoal(n, state, other):
        return (10000, other, state)

    if isGoal(n, state, player):
        return (-10000, player, state)

    if depth == 0:
        return heuristic(state, n, other, maximixing,moves)
    if maximixing:
        maxEval = -100000000
        final_move=""
        tempVal=-100000000
        for child, move in successor(state, n, player):
            eval, p, temp = minimax(child, n, depth - 1, alpha, beta, other, False,move)
            maxEval = max(maxEval, eval)
            if (maxEval == eval):
                if eval == tempVal and final_move !="":
                    tempMove = random.choice([final_move,move])
                    if(tempMove==move):
                        final_move= move
                        board= child
                else:    
                    final_move = move
                    board = child
            tempVal=maxEval        
            alpha = max(alpha, eval)

            if beta <= alpha:
                break
        return maxEval, final_move, board
    else:
        minEval = 100000000
        for (child, move) in successor(state, n, player):
            eval, p, temp = minimax(child, n, depth - 1, alpha, beta, other, True,move)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if (minEval == eval):
                final_move1 = move
                board1 = child
            if beta <= alpha:
                break
        return minEval, final_move1, board1


# TAKING INPUTS AS COMMANDLINE
n = int(sys.argv[1])
playerTurn = sys.argv[2]
state_string = sys.argv[3]
time = int(sys.argv[4])

# CONVERTING STRING TO A GAME BOARD
# print(n,playerTurn,state_string) 
sublist = []
initial_board = []
k = 0
for j in range(n + 3):
    sublist = []
    for j in range(k, k + n):
        sublist.append(state_string[j])
    initial_board.append(sublist)
    k += n

if playerTurn == "x":
    others = "o"
else:
    others = "x"

# If initial state is goal state then it will return 0 "initial_board" 
# where 0 specifies no move has been made but goal found    
if isGoal(n, initial_board, playerTurn) or isGoal(n, initial_board, others):
    b = ""
    for i in range(0, n + 3):
        for j in range(0, n):
            b += initial_board[i][j]
    print("intial board is already a win state")
    print("0", b)
else:
    for x in range(1, 10):
        eval, move, board = minimax(initial_board, n, x, -100000000, 100000000, playerTurn, True,"0")
        b = ""
#Here we convert the game board back to a string        
        for i in range(0, n + 3):
            for j in range(0, n):
                b += board[i][j]
        print (move, b)
        if eval == 10000:
            break

