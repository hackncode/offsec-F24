from math import gcd

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def decrypt_affine(a, b, ciphertext):
    m = 26  # Size of the alphabet
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        return None  # Modular inverse doesn't exist

    plaintext = []
    for ch in ciphertext:
        if ch.isalpha():
            # Decrypt character
            char_value = (a_inv * ((ord(ch) - 65 + b) % m)) % m
            plaintext.append(chr(char_value + 65))
        else:
            plaintext.append(ch)  # Keep non-alphabet characters as is
    return ''.join(plaintext)

# Load the encrypted text
encrypted_file_path = './encrypted.txt'  # Replace with your encrypted file
with open(encrypted_file_path, 'r') as file:
    encrypted_message = file.read()

# Valid ranges for a and b
valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]  # Valid values of 'a'
valid_b_values = range(1, 27)  # Valid values of 'b'

# Search for the correct decryption
with open("decryption_results.txt", "w") as output_file:
    for a in valid_a_values:
        for b in valid_b_values:
            decrypted_message = decrypt_affine(a, b, encrypted_message)
            if decrypted_message:
                output_file.write(f"a={a}, b={b}: {decrypted_message}\n")

print("Decryption attempts saved to decryption_results.txt")