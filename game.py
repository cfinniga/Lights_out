import numpy as np
import copy
import math
import time
import itertools
import random
import algebra

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

def get_matrix_from_game(n,m):
    '''
    Create n^2 x n^2 matrix for solving the game
    '''
    
    mat = np.zeros((n*n,n*n),dtype=int)

    for i in range(0,n*n):
        x = math.floor(i/n)
        y = (i)%n

        # Light up square

        mat[i][i] = 1

        if i%n != 0:
            # not left edge
            mat[i-1][i] = 1

        if i%n != n-1:
            # not right edge
            mat[i+1][i] = 1
                
        if i >= n:
            # Not top edge
            mat[i-n][i] = 1
                
        if i < n*(n-1):
            # Not bottom edge
            mat[i+n][i] = 1
    return mat
class Game_solver:
    
    def __init__(self,length,width):
        '''
        something
        '''
        self.matrix = get_matrix_from_game(length, width)
        self.game_vector = None
        self.solution = None
        self.length = length
        self.width = width

    def set_game_vector(self,game_matrix):
        '''
        Creates a vector such that each element is 1 if the corresponding square is on, otherwise 0
        '''
        self.game_vector = np.reshape(game_matrix, (self.length*self.width,1)) #.flatten('F')
    
    def solve(self,A,n,m):
        '''
        return all moves to solve the game
        '''
        A = np.concatenate((self.matrix,self.game_vector),1)
        A_tri = algebra.get_upper_triangular(A,n*m,n*m)
    
        if True: #is_upper_triangular(A_tri,n*m,n*m):
            x = algebra.back_sub(A,n*m,n*m)
        self.solution = x
        return self.solution
        
    def get_hint(self,matrix,length,width):
        '''
        return one of the moves to solve the game
        '''
        self.solve(matrix,length,width)
        indices = []
        if self.solution.any():
            for idx, item in enumerate(self.solution):
                if item == 1:
                    indices.append(idx)
        if indices:
             return random.choice(indices)
        else:
            return

class Game:
    def create_game_matrix(self):
        return create_puzzle()

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.matrix = create_puzzle(length, width)
        self.moves = create_puzzle(length, width)
        self.solver = Game_solver(length, width) # new

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
        self.solver.set_game_vector(self.matrix)

    def scramble_debug(self):
        self.matrix = np.array([[0, 0, 0], [1, 1, 0], [1, 0, 1]])
        self.solver.set_game_vector(self.matrix)
        self.init_move_matrix()
        
    def next_cell(self,row,col):
        next_row = row + 1
        next_col = col + 1
        if (row == self.width - 2):
            next_row = 0
        if (col == self.length - 2):
            next_col = 0
        return [next_row, next_col]
    
    def get_hint(self):
        hint = self.solver.get_hint(self.matrix,self.length,self.width)
        return hint
    
    def solve(self):
        return self.solver.solve(self.matrix,self.length,self.width)