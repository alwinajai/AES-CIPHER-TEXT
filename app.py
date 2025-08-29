from flask import Flask, request, jsonify, render_template_string
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64

app = Flask(__name__)

dark_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Encryptix</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap" rel="stylesheet">
    <style>
    body {
        background: linear-gradient(115deg,#121826 60%, #1a213a 100%);
        color: #f1f5f9;
        font-family: 'Rubik', Arial, sans-serif;
        margin: 0;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .main-wrap {
        max-width: 1050px;
        width: 96vw;
        border-radius: 22px;
        background: #181b28;
        box-shadow: 0 8px 36px #000a;
        display: grid; grid-template-columns: 1.25fr 1fr;
        gap: 30px;
        padding: 36px 38px 26px 38px;
    }
    .column { 
        display: flex; 
        flex-direction: column; 
        gap: 18px;
    }
    .panel {
        background: #22263b;
        border-radius: 14px;
        box-shadow: 0 2px 10px #0003;
        padding: 18px 18px 11px 18px;
        margin-bottom: 0;
        position: relative;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .panel label {
        color: #bae6fd;
        font-weight: 600;
        font-size: 1.02rem;
        margin-bottom: 4px;
        margin-top: 0;
    }
    input[type="text"], select {
        width: 100%;
        background: #23263b;
        color: #f1faee;
        border: 1.5px solid #384269;
        border-radius: 8px;
        padding: 9px 13px;
        font-size: 1rem;
        font-family: 'Rubik', Arial, sans-serif;
        margin-bottom: 8px;
        margin-top: 0;
        min-height: unset;
        height: 2.3em;
        box-sizing: border-box;
        transition: border 0.18s, box-shadow 0.15s;
    }
    textarea {
        width: 100%;
        background: #23263b;
        color: #f1faee;
        border: 1.5px solid #384269;
        border-radius: 8px;
        padding: 9px 13px;
        font-size: 1rem;
        font-family: 'Rubik', Arial, sans-serif;
        margin-bottom: 8px;
        min-height: 52px; max-height: 110px;
        box-sizing: border-box;
        transition: border 0.18s, box-shadow 0.15s;
    }
    input[readonly] {
        background: #182034;
        color: #60e4fa;
    }
    textarea[readonly] {
        background: #182034;
        color: #60e4fa;
    }
    .side-by-side { 
        display: flex; 
        gap: 10px; 
        align-items: center;
    }
    .panel select { width: 108px; background: #181c2f;}
    .btn {
        border: 2px solid #30cfd0;
        border-radius: 19px;
        background: #153448;
        font-size: 0.99rem;
        color: #e0f2f1;
        font-weight: 600;
        padding: 9px 20px;
        margin: 2px 0;
        box-shadow: 0 2px 6px #161b2140;
        cursor: pointer;
        transition: background 0.19s, border-color 0.19s;
    }
    .btn:active {
        background: #0d223a;
        border-color: #60e4fa;
        color: #bbf7ff;
    }
    .btn.primary {
        border-color: #5eead4;
        background: #23405a;
        color: #dbf4ff;
    }
    .btn-row {
        display: flex;
        gap: 12px; 
        margin-top: 8px;
    }
    .out-panel {
        background: #181c2e;
        border-radius: 14px;
        box-shadow: 0 1px 7px #0dcaf044;
        padding: 20px 15px 12px 18px;
        margin-bottom: 7px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .result-label {
        color: #6edff6;
        font-weight: 700;
        font-size: 1.06rem;
    }
    .outputbox {
        background: #101933;
        color: #fcd34d;
        font-family: 'Fira Mono', monospace;
        margin-top: 7px;
        min-height: 58px;
        font-size: 1.02rem;
        border-radius: 9px;
        padding: 13px 10px 10px 12px;
        box-shadow: 0 1px 2px #0001;
        word-break: break-all;
    }
    .output-title {
        background: #232749;
        color: #e0eaff;
        font-size: 1.28rem;
        font-weight: 600;
        border-radius: 10px 10px 0 0;
        padding: 9px 0 8px 15px;
        margin-bottom: 0;
        margin-top: 0;
    }
    .main-title {
        background: #191c29;
        color: #70d7fa;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-align: left;
        border-radius: 14px 14px 0 0;
        padding: 13px 15px 10px 0;
        margin-bottom: 10px;
        line-height: 1.21;
    }
    @media (max-width:950px) {
        .main-wrap { grid-template-columns: 1fr; padding:18px 4vw;}
        .main-title, .output-title { border-radius: 14px 14px 0 0; }
        .column { gap: 13px;}
        .panel, .out-panel {padding: 13px 4vw 8px 5vw;}
    }
    </style>
</head>
<body>
<div class="main-wrap">
    <div class="column">
        <div class="main-title">Encryptix</div>
        <div class="panel form-section">
            <label for="plain">Text to Encrypt/Decrypt:</label>
            <textarea id="plain" rows="3" placeholder="Type your message..."></textarea>
        </div>
        <div class="panel form-section">
            <div class="side-by-side">
                <label style="flex:1;">Select Key Size</label>
                <select id="keySize">
                    <option value="16">128-bit</option>
                    <option value="24">192-bit</option>
                    <option value="32">256-bit</option>
                </select>
                <button class="btn primary" type="button" onclick="generateKey()">New Key</button>
            </div>
            <label for="key">Secret Key (Base64):</label>
            <input id="key" type="text" readonly autocomplete="off" value="">
            <div class="side-by-side">
                <label style="flex:1;">IV</label>
                <button class="btn" type="button" onclick="generateIV()">New IV</button>
            </div>
            <input id="iv" type="text" readonly autocomplete="off" value="">
        </div>
        <div class="panel">
            <div class="btn-row">
                <button class="btn primary" onclick="encrypt()">Encrypt</button>
                <button class="btn" onclick="decrypt()">Decrypt</button>
            </div>
        </div>
    </div>
    <div class="column">
        <div class="output-title">Output</div>
        <div class="out-panel">
            <span class="result-label">Result:</span>
            <div id="resultDisplay" class="outputbox"></div>
        </div>
        <button class="btn primary" style="width:100%;" onclick="clearAll()">Clear All</button>
    </div>
</div>
<script>
function generateKey() {
    let size = parseInt(document.getElementById('keySize').value);
    fetch('/generate_key?size=' + size)
        .then(resp => resp.json())
        .then(data => { document.getElementById('key').value = data.key; });
}
function generateIV() {
    fetch('/generate_iv')
        .then(resp => resp.json())
        .then(data => { document.getElementById('iv').value = data.iv; });
}
function encrypt() { processAES('encrypt'); }
function decrypt() { processAES('decrypt'); }
function clearAll() {
    document.getElementById('plain').value = '';
    document.getElementById('resultDisplay').innerText = '';
    document.getElementById('key').value = '';
    document.getElementById('iv').value = '';
}
function processAES(type) {
    let text = document.getElementById('plain').value.trim();
    let key = document.getElementById('key').value;
    let iv = document.getElementById('iv').value;
    let keyLen = document.getElementById('keySize').value;
    let fmt = 'base64';
    if (!text) { alert("Please enter text!"); return; }
    if (!key) { alert("Please generate the key!"); return; }
    if (!iv) { alert("Please generate the IV!"); return; }
    fetch('/'+type, {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ text, key, iv, key_len: keyLen, output_fmt: fmt })
    }).then(resp=>resp.json())
      .then(data=>{
        document.getElementById('resultDisplay').innerText = data.error ? "Error: " + data.error :
                    (type=='encrypt'?data.ciphertext:data.plaintext);
      });
}
</script>
</body>
</html>
'''

def aes_cipher(key, iv):
    return Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())

def pad(data):
    p = padding.PKCS7(128).padder()
    return p.update(data) + p.finalize()

def unpad(data):
    u = padding.PKCS7(128).unpadder()
    return u.update(data) + u.finalize()

@app.route('/')
def home():
    return render_template_string(dark_html)

@app.route('/generate_key')
def api_key():
    size = int(request.args.get('size', '16'))
    return jsonify({'key': base64.b64encode(os.urandom(size)).decode()})

@app.route('/generate_iv')
def api_iv():
    return jsonify({'iv': base64.b64encode(os.urandom(16)).decode()})

@app.route('/encrypt', methods=['POST'])
def api_encrypt():
    try:
        data = request.json
        key = base64.b64decode(data['key'])
        iv = base64.b64decode(data['iv'])
        pt = data['text'].encode()
        cipher = aes_cipher(key, iv).encryptor()
        ct = cipher.update(pad(pt)) + cipher.finalize()
        return jsonify({'ciphertext': base64.b64encode(ct).decode()})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/decrypt', methods=['POST'])
def api_decrypt():
    try:
        data = request.json
        key = base64.b64decode(data['key'])
        iv = base64.b64decode(data['iv'])
        inp = data['text']
        ct = base64.b64decode(inp)
        cipher = aes_cipher(key, iv).decryptor()
        pt = cipher.update(ct) + cipher.finalize()
        return jsonify({'plaintext': unpad(pt).decode()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
