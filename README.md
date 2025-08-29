# AES-Encryption-Cyphertext
A sleek, modern AES encryption/decryption web tool built with Python (Flask) and the `cryptography` library. Securely generate and handle AES keys of 128, 192, or 256 bits, and encrypt/decrypt your data through a responsive, mobile-friendly, dark-themed interface.


# Technologies Used

- Python 3.7+
- [Flask](https://flask.palletsprojects.com/)
- [cryptography](https://cryptography.io/en/latest/)
- HTML5, CSS3, JavaScript (frontend/UI)


# Security
- **All cryptographic operations** use industry-standard CBC mode and PKCS7 padding.
- Secret key and IV are generated per-user, never stored.
- This tool is intended for educational, demo, or local use. For production/mission-critical cryptography, always audit and harden your deployment and secret management.

- # Features

- **AES encryption and decryption** (CBC mode) for 128/192/256-bit keys
- **One-click, secure random key and IV generation** (Base64 output)
- **User-friendly, modern dark UI**
- **Real-time results** – output displays instantly
- **No storage of sensitive data** – all data is ephemeral
- **Easy to run locally** (single Python file)

# Installation

1. **Clone the repository**
    ```
    git clone https://github.com/your-username/aes-encrypt-decrypt-utility.git
    cd aes-encrypt-decrypt-utility
    ```

2. **Install dependencies**
    ```
    pip install flask cryptography
    ```

3. **Run the app**
    ```
    python aes_flask_project.py
    ```
    Then open [http://localhost:5000](http://localhost:5000) in your browser.

# Usage

1. Enter the text you wish to encrypt or decrypt.
2. Select the AES key size (128, 192, or 256-bit).
3. Click **New Key** and **New IV** to generate a cryptographically secure key and IV.
4. Click **Encrypt** or **Decrypt** to process your data.
5. Use **Clear All** to reset all input and output fields.

> **Note:** The key length and IV are handled properly for every operation. All cryptography is server-side using Python's `cryptography` library.
