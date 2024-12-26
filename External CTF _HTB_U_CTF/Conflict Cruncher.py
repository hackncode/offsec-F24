import ast

# Input two dictionaries as strings
dict1_str = input().strip()
dict2_str = input().strip()

# Convert the strings to dictionaries using literal_eval
dict1 = ast.literal_eval(dict1_str)
dict2 = ast.literal_eval(dict2_str)

# Merge the dictionaries
# Keys from dict2 overwrite those in dict1 when conflicts occur
merged_dict = dict1.copy()
merged_dict.update(dict2)

# Print the merged dictionary
print(merged_dict)