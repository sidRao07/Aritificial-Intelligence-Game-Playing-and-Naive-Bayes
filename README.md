FORMULATING THE SEARCH PROBLEM:

INITIAL STATE: 

Initial state could be a empty board of size (n+3) x n where n=5 for beginners or could be any filled state. 
For instance: for n=3
We can have a board: 

		. . .                          	. . .
		. . .				o . .
		. . .				x . o
		. . .				o o o
		. . .				x x x
		. . .				x x o

              An empty board		 Board at a random state

SUCCESSOR: 

There are two possible moves, drop and rotate. 
Drop: Choose one of the n columns and drop a pebble into the column. The pebble falls to occupy the bottom most empty square. 
The player is not allowed to chose a column that is already full.
Rotate: Choose one of the n columns, remove the pebble from the bottom of that column so that all pebbles fall down by one and 
then drop the same pebble into the top of that column.


If board state is : 

. . .
o . .
x . o
o o o
x x x 
x x o


Possible successors are:  

. . .          . . .            . . .       . . .      . . .      x . . 
x . .          o . .		o . .       o . .      o . x      o . . 
o . o	       x . o		x . o       x x o      x . o      x . o 
x o o          o x o		o o o       o o o      o o o      o o o 
o x x          x o x		x x o       x x x      x x x      x x x 
x x o          x x o		x x x       x x o      x x x      x x o 
                           
 -1              -2             -3          2           3         1
 
| .  | .  | .  |               	    
|----|----|----|             
| x  | .  | .  |             -1
| o  | .  | o  |                          
| o  |  x | x  |             
| x  |  x | o  |       

| .  | .  | .  |               	    
|----|----|----|             
| x  | .  | o  |             
| o  | x  | o  |              -2           
| x  |  o | x  |             
| x  |  x | o  |

| .  | .  | .  |               	    
|----|----|----|             
| o  | .  | .  |             
| x  | .  | o  |              -3            
| o  | o  | o  |             
| x  |  x | o  |
| x  |  x | x  |

| .  | .  | .  |               	    
|----|----|----|             
| o  | .  | .  |              2
| x  | x  | o  |                          
| o  | o  | o  |             
| x  |  x | x  |
| x  |  x | o  |

| .  | .  | .  |               	    
|----|----|----|             
| o  | .  | x  |             
| x  | .  | o  |               3          
| o  | o  | o  |             
| x  |  x | x  |
| x  |  x | x  |
 
| x  | .  | .  |               	    
|----|----|----|             
| o  | .  | .  |             
| x  | .  | o  |                          
| o  | o  | o  |             1
| x  |  x | x  |
| x  |  x | o  |
 
GOAL STATE:

Possible goal states are: 

x . .          . . x            . . .       o . .      etc
x x .          o x o		x x x       o . .      
o x x	       x o o		x x o       o x o      
x o o          o x o		o o o       o o o     
o x x          x o x		x x o       x x x     
x x o          x x o		x x x       x x o     


HOW WE SOLVED THE PROBLEM:

STEP 1: Input the size of the board, first player, initial board as a string and the time cutoff.

STEP 2: Convert the string to a game board. [Lines 225 to 232]

STEP 3: If initial player is "X" assign the other player as "O" and vice versa.

STEP 4: Check if initial board state is already a goal state or not. If it is already a goal state then we return value "0" for 
the move along with the original board. The program terminates there.

STEP 5: If the STEP 4 is not true then the board is passed to the minimax method which runs the minimax algorithm. 
        POINT TO NOTE: We are performing Iterative Deepening Search (IDS) till depth= 25. The depth (variable x) is passed to the minimax method as the depth parameter.
		       Alpha value is passed as -100000000 while beta is taken + 100000000

STEP 6: Generating successors, computations and giving optimal mov are performed according to the methods given below:


def isGoal() 
In this method we check if the nxn board is a goal state or not i.e. all rows, all columns and both the diagonals are checked for 
turn = x or o. The all() method of python is a standard library function which returns True when all elements in the given iterable are true. For checking all elements in column a temporary list lcol[] is taken which stores the elements of each column and then all() method is used to check if all elements are same in that list. Once this is done, the column is changed and the lcol[] is reset to empty by function del. The same procedure is applied for the diagonals except that the conditions are different for left (i==j) and right (i+j==n-1) diagonals.


def successor()
SUCCESSOR RETURNS ALL THE SUCCESSORS OF THE CURRENT STATE
This functions combines the output of rotate and drop into one and returns it the MINMAX. A check is made to ensure that the number of pebbles for a particular palyer does not increase n*(n+3)/2  

                            |-------> rotate()
    successor() ------------|
                            |-------> drop()


def rotate()
METHOD TO ROTATE THE BOARD
First loop (0 to n) is applied to change columns while the internal loop ((n+3)-1 to 0) is
iterating in reverse which is shifting each element down by 1.
The last element at the end of the column is removed and is stored in removed_element.
Once the elements are shifted by 1 we drop the removed element into the first column.
 Another loop (j=(n+3)-1 to 0) is iterating in reverse and checks the first empty position in the column
starting from the bottom. At the first empty position the removed element is inserted. 


def drop()
METHOD TO DROP THE BOARD
For every row from the bottom we check if there is any empty state.
if so then we drop a piece into the particular column and then blacklist the cloumn.
This step is scontinued until all possible drop moves are made. 

def heuristic()
HEURISTIC FUNCTION
We check the current state of the board and based on the player's turn we are assigning max value of +100 for the number of pieces the max player has on every row, column and diagonals while -50 for every opponent's piece. We consider this for nxn board and discard the last three rows. However, there is a exception that we also consider the value for the piece which is present in the last row because that is the piece which will be rotated. We return the max Of all the sums as the heuristic if it is max's turn and negative of the max if it is min's turn.
Heuritic for x will be = max(heuristic value of 1st row to nth row,heuristic value of 1st column to nth column, heuristic of 
right diagonal, heuristic value of left diagonal,heuristic value of last (n+3)rd row.
 
  
 





