import urllib.parse

# Read the encoded content from a file
with open('encoded_string.txt', 'r') as f:
    data = f.read()

# Recursively decode until no further decoding is possible
decoded = data
while True:
    temp = urllib.parse.unquote(decoded)
    if temp == decoded:  # Stop if no changes occur
        break
    decoded = temp

# Save the fully decoded content to a file
with open('fully_decoded_output.txt', 'w') as f:
    f.write(decoded)

print("Decoded content saved to fully_decoded_output.txt")

