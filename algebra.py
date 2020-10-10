import numpy as np

def get_upper_triangular(A,n,m):
    '''
    input:
    A - n by n matrix
    output:
    matrix A in upper triangular form
    Modified from regular gaussian elimination algorithm
    '''
    if n != m:
        return
    
    # pivot column
    pivot_col = 0
    
    # Iterate through rows until the pivot col entry is 1
    for pivot_col in range(0,m): # m+1?
        max_i = pivot_col
        
        for row in range(pivot_col,n):

            if A[row,pivot_col] == 1: 
                max_i = row
                break

        if A[max_i,pivot_col] == 1:
            # Swap rows i and max_i
            A[[pivot_col, max_i]] = A[[max_i, pivot_col]]
            
            for u in range(pivot_col+1,m):
                if A[u][pivot_col] == 1:
                    A[u] = (A[pivot_col]+A[u])%2
        #else:
            # more than one solution
            # print("More than one solution for var")
            # print(A)
            
    return A

def back_sub(A,n,m):
    '''
    A an n by m+1 matrix, in upper triangular form
    '''
    
    x = np.zeros((n,), dtype=int)
    for i in range(n-1,-1,-1):
        if A[i,i] == 1:
            x[i] = A[i,n]
            for j in range(i+1,n):
                x[i] = (x[i] - x[j]*A[i][j]) % 2
        #else:
        #    print("error :(")
    return x
    

def is_upper_triangular(A, n, m):
    '''
    A an n by m matrix, in upper triangular form
    '''
    #A = np.array([[1, 0, 0, 1], [0, 1, 1, 0], [0, 0, 1, 1]])
    #n = 3
    #m = 3
    min = 0
    for row in A[1:]:
        for i in range(0,n):
            if row[i] == 1 and i > min:
                min = i
                break
            elif i <= min and row[i] == 1:
                return False
            elif row[i] != 0:
                return False
    return True