import time
import random

# Helper: Pad matrix to the next power of 2 for Divide & Conquer / Strassen
def pad_matrix(matrix, new_size):
    padded = [[0] * new_size for _ in range(new_size)]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            padded[i][j] = matrix[i][j]
    return padded

# Helper: Helper matrix operations
def add_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def subtract_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def split_matrix(A):
    n = len(A) // 2
    return (
        [row[:n] for row in A[:n]],  # A11
        [row[n:] for row in A[:n]],  # A12
        [row[:n] for row in A[n:]],  # A21
        [row[n:] for row in A[n:]]   # A22
    )

# 1. Approach: Naive Matrix Multiplication O(n^3)
def naive_multiply(A, B):
    n, m, p = len(A), len(A[0]), len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]
    return C

# 2. Approach: Divide and Conquer Multiplication O(n^3)
def dc_multiply_recursive(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)
    
    C11 = add_matrices(dc_multiply_recursive(A11, B11), dc_multiply_recursive(A12, B21))
    C12 = add_matrices(dc_multiply_recursive(A11, B12), dc_multiply_recursive(A12, B22))
    C21 = add_matrices(dc_multiply_recursive(A21, B11), dc_multiply_recursive(A22, B21))
    C22 = add_matrices(dc_multiply_recursive(A21, B12), dc_multiply_recursive(A22, B22))
    
    # Combine quarters
    C = []
    for i in range(n // 2):
        C.append(C11[i] + C12[i])
    for i in range(n // 2):
        C.append(C21[i] + C22[i])
    return C

def dc_multiply(A, B):
    # Determine the next power of 2 for padding
    max_dim = max(len(A), len(A[0]), len(B[0]))
    next_pow2 = 1
    while next_pow2 < max_dim:
        next_pow2 *= 2
        
    padded_A = pad_matrix(A, next_pow2)
    padded_B = pad_matrix(B, next_pow2)
    
    padded_C = dc_multiply_recursive(padded_A, padded_B)
    
    # Slice back to original dimensions
    return [row[:len(B[0])] for row in padded_C[:len(A)]]

# 3. Approach: Strassen's Algorithm O(n^2.81)
def strassen_multiply_recursive(A, B):
    n = len(A)
    if n <= 2:  # Base case switch to naive for efficiency at low dimensions
        return naive_multiply(A, B)
        
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)
    
    P1 = strassen_multiply_recursive(A11, subtract_matrices(B12, B22))
    P2 = strassen_multiply_recursive(add_matrices(A11, A12), B22)
    P3 = strassen_multiply_recursive(add_matrices(A21, A22), B11)
    P4 = strassen_multiply_recursive(A22, subtract_matrices(B21, B11))
    P5 = strassen_multiply_recursive(add_matrices(A11, A22), add_matrices(B11, B22))
    P6 = strassen_multiply_recursive(subtract_matrices(A12, A22), add_matrices(B21, B22))
    P7 = strassen_multiply_recursive(subtract_matrices(A11, A21), add_matrices(B11, B12))
    
    C11 = add_matrices(subtract_matrices(add_matrices(P5, P4), P2), P6)
    C12 = add_matrices(P1, P2)
    C21 = add_matrices(P3, P4)
    C22 = subtract_matrices(subtract_matrices(add_matrices(P5, P1), P3), P7)
    
    C = []
    for i in range(n // 2):
        C.append(C11[i] + C12[i])
    for i in range(n // 2):
        C.append(C21[i] + C22[i])
    return C

def strassen_multiply(A, B):
    max_dim = max(len(A), len(A[0]), len(B[0]))
    next_pow2 = 1
    while next_pow2 < max_dim:
        next_pow2 *= 2
        
    padded_A = pad_matrix(A, next_pow2)
    padded_B = pad_matrix(B, next_pow2)
    
    padded_C = strassen_multiply_recursive(padded_A, padded_B)
    return [row[:len(B[0])] for row in padded_C[:len(A)]]

def run_benchmark():
    print("=== MATRIX MULTIPLICATION SHOWDOWN ===")
    
    # Take user options
    choice = input("Enter '1' to input manual matrices or '2' for auto-generated random test: ")
    
    if choice == '1':
        r1 = int(input("Enter rows for Matrix A: "))
        c1 = int(input("Enter columns for Matrix A: "))
        r2 = int(input("Enter rows for Matrix B: "))
        c2 = int(input("Enter columns for Matrix B: "))
        
        if c1 != r2:
            print("Error: Columns of A must equal Rows of B!")
            return
            
        print("Enter elements for Matrix A row by row (space separated):")
        A = [list(map(int, input().split())) for _ in range(r1)]
        print("Enter elements for Matrix B row by row (space separated):")
        B = [list(map(int, input().split())) for _ in range(r2)]
    else:
        # Default size that highlights the efficiency curves without freezing terminal execution
        size = 64 
        print(f"Generating random matrices of size {size}x{size}...")
        A = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]
        B = [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]

    # Benchmark Naive
    t0 = time.perf_counter()
    res_naive = naive_multiply(A, B)
    time_naive = (time.perf_counter() - t0) * 1000 # ms
    
    # Benchmark Divide & Conquer
    t0 = time.perf_counter()
    res_dc = dc_multiply(A, B)
    time_dc = (time.perf_counter() - t0) * 1000 # ms
    
    # Benchmark Strassen
    t0 = time.perf_counter()
    res_strassen = strassen_multiply(A, B)
    time_strassen = (time.perf_counter() - t0) * 1000 # ms
    
    # Verification Check
    is_valid = (res_naive == res_dc == res_strassen)
    status = "PASSED" if is_valid else "FAILED"
    
    # Determine the absolute fastest method
    times = {
        "Naive Matrix Multiplication": time_naive,
        "Divide and Conquer": time_dc,
        "Strassen's Algorithm": time_strassen
    }
    fastest_method = min(times, key=times.get)

    # Print Expected Output Format
    print("\nMethod                       Time Taken")
    print("-" * 48)
    print(f"Naive Matrix Multiplication  {time_naive:.2f} ms")
    print(f"Divide and Conquer           {time_dc:.2f} ms")
    print(f"Strassen's Algorithm         {time_strassen:.2f} ms")
    print("-" * 48)
    print(f"Verification Status: {status}")
    print(f"Fastest Method: {fastest_method}")

if _name_ == "_main_":
    run_benchmark()
