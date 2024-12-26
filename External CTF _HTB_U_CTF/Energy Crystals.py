# Read inputs as raw strings
energy_crystals_str = input().strip()
target_energy_str = input().strip()

# The energy crystals might be given in a format like: [1, 2, 3]
# Remove brackets and spaces, then split by comma
cleaned_str = energy_crystals_str.strip("[] \t")
# Handle the case where cleaned_str might be empty
if cleaned_str:
    energy_crystals = list(map(int, cleaned_str.split(',')))
else:
    energy_crystals = []

# Convert the target energy string to an integer
target_energy = int(target_energy_str)

# Initialize DP array
dp = [0] * (target_energy + 1)
dp[0] = 1  # One way to make 0 (choose no crystals)

# Calculate the number of ways using classic coin change DP
for crystal in energy_crystals:
    for energy in range(crystal, target_energy + 1):
        dp[energy] += dp[energy - crystal]

# Print the result
print(dp[target_energy])