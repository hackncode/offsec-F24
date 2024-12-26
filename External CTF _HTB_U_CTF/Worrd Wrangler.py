import re
from collections import Counter

# Input the text as a single string
input_text = input().strip()

# Convert to lowercase
lower_text = input_text.lower()

# Extract words using regular expressions (alphabetic characters only)
words = re.findall(r"[a-z]+", lower_text)

# Count the frequencies of each word
word_counts = Counter(words)

# Find the most common word(s)
most_common_word, _ = word_counts.most_common(1)[0]

# Print the most common word
print(most_common_word)