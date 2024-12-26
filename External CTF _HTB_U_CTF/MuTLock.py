import random
import string
import base64

def generate_key(seed, length=16):
    random.seed(seed)
    key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    return key

def polyalphabetic_decrypt(ciphertext, key):
    key_length = len(key)
    plaintext = []
    for i, char in enumerate(ciphertext):
        key_char = key[i % key_length]
        decrypted_char = chr((256 + ord(char) - ord(key_char)) % 256)
        plaintext.append(decrypted_char)
    return ''.join(plaintext)

def xor_decipher(ciphertext_bytes, xor_key):
    return bytes([c ^ xor_key for c in ciphertext_bytes]).decode(errors="ignore")

def is_valid_base64(s):
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode()
    except Exception:
        return False

def decrypt_even_half(hex_ciphertext):
    # Even half uses xor_key = 42
    ciphertext_bytes = bytes.fromhex(hex_ciphertext)
    xor_key = 42
    base64_text = xor_decipher(ciphertext_bytes, xor_key)
    if is_valid_base64(base64_text):
        decoded_text = base64.b64decode(base64_text).decode(errors="ignore")
        return decoded_text
    return None

def decrypt_odd_half(hex_ciphertext):
    # Odd half uses key_seed=42 and unknown xor_key
    ciphertext_bytes = bytes.fromhex(hex_ciphertext)
    for xor_key in range(1, 256):
        base64_text = xor_decipher(ciphertext_bytes, xor_key)
        if is_valid_base64(base64_text):
            decoded_text = base64.b64decode(base64_text).decode(errors="ignore")
            return decoded_text, xor_key
    return None, None

def brute_force_key_seed(ciphertext, known_plaintext):
    # Try all seeds to find which yields plaintext containing known_plaintext
    for seed in range(1, 1001):
        key = generate_key(seed)
        decrypted_text = polyalphabetic_decrypt(ciphertext, key)
        if known_plaintext in decrypted_text:
            return decrypted_text, seed
    return None, None

# Given ciphertext lines from output.txt
encrypted_flags = [
    "00071134013a3c1c00423f330704382d00420d331d04383d00420134044f383300062f34063a383e0006443310043839004315340314382f004240331c043815004358331b4f3830",
    "5d1f486e4d49611a5d1e7e6e4067611f5d5b196e5b5961405d1f7a695b12614e5d58506e4212654b5d5b196e4067611d5d5b726e4649657c5d5872695f12654d5d5b4c6e4749611b"
]

first_half_candidate = decrypt_even_half(encrypted_flags[0])
second_half_candidate = decrypt_even_half(encrypted_flags[1])

if first_half_candidate:
    even_half = first_half_candidate
    odd_half, odd_xor_key = decrypt_odd_half(encrypted_flags[1])
else:
    even_half = decrypt_even_half(encrypted_flags[1])
    odd_half, odd_xor_key = decrypt_odd_half(encrypted_flags[0])

if even_half and odd_half:
    print(f"[DEBUG] Even half (polyalphabetic ciphertext): {even_half}")
    print(f"[DEBUG] Odd half (polyalphabetic ciphertext): {odd_half}")
    print(f"[DEBUG] Odd half XOR key: {odd_xor_key}")

    # Decrypt odd half fully (key_seed=42)
    random.seed(42)
    chars = string.ascii_letters + string.digits
    known_key = ''.join(random.choice(chars) for _ in range(16))
    odd_plaintext = polyalphabetic_decrypt(odd_half, known_key)
    print(f"[DEBUG] Odd half plaintext: {odd_plaintext}")

    # Use "ion" as known plaintext to continue from "encrypt" → "encryption"
    flag_even_half, seed = brute_force_key_seed(even_half, "ion")
    if flag_even_half:
        print(f"[DEBUG] Even half decrypted with seed {seed}: {flag_even_half}")
        full_flag = odd_plaintext + flag_even_half
        print("Decrypted full flag:", full_flag)
    else:
        print("Failed to decrypt even half.")
else:
    print("Failed to identify even and odd halves.")

