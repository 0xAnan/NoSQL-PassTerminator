Here's a complete and professional `README.md` for your GitHub repository, tailored to the current script you're using:

---

## 🔐 NoSQL PassTerminator

*Automated Blind NoSQL Injection Password Cracker for MongoDB-style queries*
by **0xTensai**

---

### 🧠 Description

**NoSQL BruteMaster 3000** is a blind NoSQL injection tool that performs character-by-character brute-forcing on password fields using JavaScript-style injection payloads. It works by detecting the password length, then brute-forcing each character based on server responses.

---

### ⚙️ Features

* 🔍 Blind password length detection
* 🧩 Character-by-character brute-force on NoSQL injection points
* ✅ Supports POST requests from raw HTTP request files (Burp-style)
* 🎯 Uses fail-string logic to infer correct guesses
* 💡 Customizable charset and casing

---

### 📥 Requirements

* Python 3.x
* `requests` library
  Install with:

```bash
pip install requests
```

---

### 🚀 Usage

```bash
python3 nosql.py -r request.txt -f "user not found" -p user -n administrator
```

---

### 🧾 Arguments

| Flag                  | Description                                                     |
| --------------------- | --------------------------------------------------------------- |
| `-r`, `--request`     | Path to raw HTTP request file (Burp format)                     |
| `-f`, `--fail-string` | Failure indicator text in the response (e.g., "user not found") |
| `-p`, `--param`       | Name of the POST parameter to inject into (e.g., `user`)        |
| `-n`, `--username`    | The username whose password you want to brute-force             |
| `--max-length`        | Maximum password length to attempt (default: 30)                |

---

### 📦 Example

```bash
python3 nosql.py \
  -r login.req \
  -f "Could not find user" \
  -p user \
  -n administrator
```

The tool will:

* Detect the password length of the `administrator` account
* Brute-force the password using blind injection
* Print the password once found

---

### 🔠 Character Set Options (interactive)

When prompted:

* Choose charset:

  * 1 = alphabets only (a–z or A–Z)
  * 2 = alphabets + numbers
  * 3 = alphabets + numbers + special characters
* Choose casing:

  * 1 = lowercase
  * 2 = uppercase
  * 3 = both

---

### 🧪 Injection Logic

For each character:

```js
username' && this.password[0] == 'a' || 'a'=='b
```

---

### ⚠️ Disclaimer

This tool is intended **only** for educational and authorized security testing purposes.
**Do not** use it on systems you don't have permission to test.

---

### 👨‍💻 Author

Built with 💻 by [**0xTensai**](https://github.com/0xTensai)

---

Let me know if you'd like a sample Burp-style `.req` file or want a logo/badge for the repo.
