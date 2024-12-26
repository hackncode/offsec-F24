# Input two arrays as strings
signals = input()  
weights = input()  

# Evaluate the string inputs to lists
signals = eval(signals)
weights = eval(weights)

# Compute the modified signals by element-wise multiplication of signals and weights
modified_signals = [s * w for s, w in zip(signals, weights)]

# Initialize variables to keep track of the maximum product subarray
max_prod = min_prod = result = modified_signals[0]

# Use the dynamic programming approach to find the maximum product subarray
for num in modified_signals[1:]:
    # When the current number is negative, swapping max and min will yield the highest product
    if num < 0:
        max_prod, min_prod = min_prod, max_prod

    # Update the current max and min products
    max_prod = max(num, max_prod * num)
    min_prod = min(num, min_prod * num)

    # Update the global maximum product found so far
    result = max(result, max_prod)

# Print the maximum stability score
print(result)
