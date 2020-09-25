import numpy as np
import copy
import math
import time
import itertools
import queue

def create_puzzle(rows, cols):
    matrix = np.arange(rows * cols)
    matrix = matrix.reshape(rows, cols)
    matrix[:] = 0
    return matrix

def print_2d_matrix(matrix):
    print(matrix)

def perform_move(matrix, length, width, x, y):
    '''
    inputs:
        the x,y coordinate to invert
    perform_move - invert current tile, and the left, right, up, down tiles

    returns:
        nothing
    '''
    matrix[x][y] = not matrix[x][y]  # double check this
    if (x != 0):
        matrix[x - 1][y] = not matrix[x - 1][y]
    if (x != (width - 1)):
        matrix[x + 1][y] = not matrix[x + 1][y]
    if (y != 0):
        matrix[x][y - 1] = not matrix[x][y - 1]
    if (y != (length - 1)):
        matrix[x][y + 1] = not matrix[x][y + 1]
        
def is_solved(matrix):
    '''
    checks if the game is solved
    returns:
        False if an entry is 1
    '''
    is_solved = True
    for col in matrix:
        for row in col:
            if (row == 1):
                return False
    return is_solved

def next_cell(x, y, width):
    if (x == width - 1):
        x = 0
        if (y == width - 1):
            return None
        else:
            y = y + 1
    else:
        x = x + 1
    return [x,y]

class Game:
    def create_game_matrix(self):
        return create_puzzle()

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.matrix = create_puzzle(length, width)
        self.moves = create_puzzle(length, width)

    def init_move_matrix(self):
        '''
        init_move_matrix - create a zeros matrix to store moves
        '''
        for i in range(0, self.width):
            for j in range(0, self.length):
                rand_value = np.random.choice([0, 1])
                self.moves[i][j] = rand_value        

    def scramble(self):
        '''
        scramble - randomly generate a 1 or 0 value for each tile in the grid
        add the value to the corresponding tiles.
        '''
        self.init_move_matrix()
        for x in range(0,self.length):
            for y in range(0,self.width):
                if (self.moves[x][y] == 1):
                     perform_move(self.matrix,self.length, self.width, x, y)

    def next_cell(self,row,col):
        next_row = row + 1
        next_col = col + 1
        if (row == self.width - 2):
            next_row = 0
        if (col == self.length - 2):
            next_col = 0
        return [next_row, next_col]

class Stack:
    '''
    This Stack class was taken from:
    http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaStackinPython.html
    '''
    def __init__(self):  
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
         return len(self.items)

def bitcount(n):
    '''
    Adapted from:
    https://stackoverflow.com/questions/8871204/count-number-of-1s-in-binary-representation
    '''
    count = 0
    for idx in range(0,len(n)):
        count = count + int(n[idx])
    return count

def bitcount_np(m, width):
    '''
    Adapted from:
    https://stackoverflow.com/questions/8871204/count-number-of-1s-in-binary-representation
    '''
    count = 0
    for idx in range (0,(width -1)):
        for j in range (0,(width -1)):
            count = count + int(m[idx][j])
    return count

def bfs(matrix,width):#, k):
    '''
    The combinatorics part of this function is taken from stack overflow
    https://stackoverflow.com/questions/1851134/generate-all-binary-strings-of-length-n-with-k-bits-set#2075867
    '''    
    matrix = copy.deepcopy(matrix)
    n = width*width
    bfs_queue = queue.Queue()
    prev_move = [0]* n
    
    counter = 0
    for idx in range (0, n+1):
        for bits in itertools.combinations(range(n), idx):
            s = ['0'] * n
            for bit in bits:
                s[bit] = '1'
            bfs_queue.put(s)
            
        for i in range (0,bfs_queue.qsize()):
            test_move = bfs_queue.get()
            
            for pos in range (len(test_move),0,-1):
                if ((int(test_move[pos-1])+int(prev_move[pos-1])%2) == 1):
                    row = math.floor((pos-1)/width)
                    col = pos - (row)*(width) - 1
                    perform_move(matrix,width,width,row,col)
                    counter = counter + 1
            if (is_solved(matrix)):
                bits = bitcount(test_move)
                return [bits,counter]
            else:
                prev_move = test_move
    
def dfs(puzzle, width):
    if not width:
        return
    n = width*width
    dfs_stack = Stack()
    matrix = copy.deepcopy(puzzle)
    
    # Create a stack
    for i in range(2**n,0,-1):
        value = bin(i)[2:]
        value = "0" * (n-len(value)) + value
        dfs_stack.push(value)
    
    # After an iteration, store the move that was previously tried
    prev_move = [0]* n
    
    # Pop items and test
    counter = 0
    for i in range (0, dfs_stack.size()):
        move = dfs_stack.pop()
        for pos in range (len(move),0,-1):
            if ((int(move[pos-1])+int(prev_move[pos-1])%2) == 1):
                row = math.floor((pos-1)/width)
                col = pos - (row)*(width) - 1
                perform_move(matrix,width,width,row,col)
                counter = counter + 1
        if (is_solved(matrix)):
            bits = bitcount(move)
            return [bits, counter]
        else:
            prev_move = move
    return

def chase_lights(matrix,width):
    solution = np.zeros((width,width))
    for y in range(0, width - 1):
        for x in range(0, width):
            if (matrix[y][x] == 1):
                #solution matrix is incorrect
                solution[y][x] = 1
                perform_move(matrix,width,width,y+1,x)
'''
def lut(row):
    if (row=="10001"):
        return "11000"
    elif(row == "01010"):
        return "10010"
    elif(row == "11100"):
        return "01000"
    elif(row == "00111"):
        return "0010"
    elif(row == "10110"):
        return "00001"
    elif(row == "01101"):
        return "10000"
    elif(row=="11011"):
        return "00100"

def challenge_task(m,width):
    matrix = copy.deepcopy(m)
    print("hi",matrix)
    #matrix = np.array([[0,1,1,0],[1,0,0,1],[0,1,0,1],[1,1,0,0]])
    print(matrix)
    solution = np.zeros((width,width))
    chase_lights(matrix,width)
    print(matrix)
    print("sol",solution)
    #use a lookup table
    if (is_solved(matrix)):
        return solution
    else:
        lut(matrix[:][width-1])
    '''
def a_star(matrix,width):
    '''
    Tries solutions starting with combinations of the minimum number of moves:
    number_lights/5
    '''
    n = width**2
    counter = 0
    prev_move = [0]* n
    a_queue = queue.Queue()
    lights_on = bitcount_np(matrix,width)
    min_moves = math.ceil(lights_on/5)
    max_moves = n
    
    # Start to look for solutions halfway between the minimum and maximum number of moves
    # Then continue average + 1, average - 2, average + 3
    for index in range (min_moves,max_moves):
        for bits in itertools.combinations(range(n), index):
            
            s = ['0'] * n
            for bit in bits:
                s[bit] = '1'
            a_queue.put(s)
        
        # Place solutions on a queue and then test themn
        for i in range (0,a_queue.qsize()):
            test_move = a_queue.get()
            for pos in range (len(test_move),0,-1):
                if ((int(test_move[pos-1])+int(prev_move[pos-1])%2) == 1):
                    row = math.floor((pos-1)/width)
                    col = pos - (row)*(width) - 1
                    perform_move(matrix,width,width,row,col)
                    counter = counter + 1
            if (is_solved(matrix)):
                bits = bitcount(test_move)
                return [bits,counter]
            else:
                prev_move = test_move
    
def main():
    print("Starting Lights Out!\n")
    '''
    Initialize the counters for 100 random puzzles
    '''
    length = 4
    width = length

    bfs_total_steps = 0
    dfs_total_steps = 0
    a_total_steps = 0
    
    bfs_min_steps = 0
    dfs_min_steps = 0
    a_min_steps = 0
    
    bfs_time = 0
    dfs_time = 0
    a_time = 0
    
    '''
    Loop through 100 random puzzles
    '''
    for tests in range (0,100):
        # Initialize a random matrix
        game = Game(length, width)
        game.scramble()
        #print("Solve the puzzle:")
        #print(game.matrix)
        
        # Perform 100 Depth First Search
        start_time = time.clock()
        dfs_result = dfs(game.matrix, length)
        end_time = time.clock()
        dfs_min_steps = dfs_min_steps + dfs_result[0]
        dfs_total_steps = dfs_total_steps + dfs_result[1]
        dfs_time = dfs_time + end_time-start_time
        
        # Perform 100 Breadth First Search
        start_time = time.clock()
        bfs_result = bfs(game.matrix,width)
        end_time = time.clock()
        bfs_min_steps = bfs_min_steps + bfs_result[0]
        bfs_total_steps = bfs_total_steps + bfs_result[1]
        bfs_time = bfs_time + end_time-start_time

        # Perform 100 A* Search
        start_time = time.clock()
        a_result = a_star(game.matrix,width)
        end_time = time.clock()
        a_time = a_time + end_time-start_time
        a_min_steps = a_min_steps + a_result[0]
        a_total_steps = a_total_steps + a_result[1]
        
    print("")
    print("Total number of steps used 100 times")
    print("bfs:",bfs_total_steps)
    print("dfs:",dfs_total_steps)
    print("a star:",a_total_steps)
    print("")
    print("Minimum number of steps in the solutions, 100 times")
    print("bfs:",bfs_min_steps)
    print("dfs:",dfs_min_steps)
    print("a star:",a_min_steps)
    print("")
    print("Total length of time for 100 algorithms")
    print("bfs:",bfs_time,"seconds")
    print("dfs:",dfs_time,"seconds")
    print("a star:",a_time,"seconds")
    print("The end.")

if __name__ == '__main__':
    main()
