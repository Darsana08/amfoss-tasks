# Task 09: Matrix Multiplication Showdown

### 🧠 Algorithms Implemented & Time Complexities
1. *Naive Method ($O(n^3)$):* Uses standard row-by-column dot products across nested iterative loops.
2. *Divide and Conquer ($O(n^3)$):* Recursively breaks down matrices into 4 sub-quadrants, computing 8 distinct sub-multiplications.
3. *Strassen's Algorithm ($O(n^{2.81})$):* Uses algebraic manipulation to reduce the recursive matrix multiplication count from 8 down to 7, resulting in sub-cubic time complexity.

### 🛠️ Verification & Execution Details
*   *Matrix Configuration Constraints:* The script dynamically pads irregular input dimensions to matching powers of 2 for correct recursive quad-splitting, cleanly extracting the true dimensions before verification.
*   *Benchmarking Strategy:* Employs precision time mapping via Python's time.perf_counter() to parse structural latency down to millisecond steps.
*
