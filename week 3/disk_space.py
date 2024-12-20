goal = 2147483647
total_moves = 0

for arg1 in range(1, 50):
    total_moves = (2 ** arg1) - 1  # Calculate total_moves using the formula T(n) = 2^n - 1
    
    if total_moves == goal:
        print(f"Matches at {arg1}.")
        break
