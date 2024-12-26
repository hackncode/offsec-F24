# Read the input string
input_str = input().strip()
# Split the string into a list of numbers
numbers = input_str.split()

seen = set()
result = []

for num in numbers:
    if num not in seen:
        seen.add(num)
        result.append(num)

print(" ".join(result))