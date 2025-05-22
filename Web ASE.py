from flask import Flask, render_template_string, request, send_file, redirect, url_for
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

template = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AES File Encryptor/Decryptor</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background: linear-gradient(to right, #4facfe, #00f2fe);
      font-family: 'Segoe UI', sans-serif;
      min-height: 100vh;
    }
    .container {
      max-width: 600px;
      margin-top: 60px;
    }
    .card {
      padding: 40px;
      border-radius: 20px;
      background: white;
      box-shadow: 0 6px 30px rgba(0,0,0,0.15);
    }
    .btn {
      width: 48%;
    }
    .form-label {
      font-weight: 600;
    }
    .download-box {
      margin-top: 20px;
      text-align: center;
    }
  </style>
</head>
<body>
<div class="container">
  <div class="card">
    <h3 class="mb-4 text-center text-primary">🔐 AES 128-bit File Encryptor/Decryptor</h3>
    <form method="POST" action="/" enctype="multipart/form-data">
      <div class="mb-3">
        <label class="form-label">📂 Chọn file</label>
        <input class="form-control" type="file" name="file" required>
      </div>
      <div class="mb-3">
        <label class="form-label">🔑 Nhập khóa (chuỗi tùy ý)</label>
        <input class="form-control" type="text" name="key" required placeholder="VD: my_secret_key_123">
      </div>
      <div class="d-flex justify-content-between">
        <button class="btn btn-outline-primary" name="action" value="encrypt">🔒 Mã hóa</button>
        <button class="btn btn-outline-success" name="action" value="decrypt">🔓 Giải mã</button>
      </div>
    </form>
    {% if filename %}
    <div class="alert alert-info download-box">
      ✅ Xử lý thành công! <br>
      <a class="btn btn-success mt-2" href="{{ url_for('download_file', filename=filename) }}">📥 Tải file kết quả</a>
    </div>
    {% endif %}
  </div>
</div>
</body>
</html>
'''

# Mã hóa AES
def aes_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return cipher.nonce + tag + ciphertext

# Giải mã AES
def aes_decrypt(data: bytes, key: bytes) -> bytes:
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

@app.route("/", methods=["GET", "POST"])
def index():
    filename = None
    if request.method == "POST":
        uploaded_file = request.files["file"]
        raw_key = request.form["key"].strip()
        action = request.form["action"]

        if not raw_key:
            return "❌ Vui lòng nhập khóa bất kỳ.", 400

        # Băm SHA-256 và lấy 16 bytes đầu để tạo khóa AES-128
        key = hashlib.sha256(raw_key.encode()).digest()[:16]
        file_data = uploaded_file.read()

        try:
            if action == "encrypt":
                result = aes_encrypt(file_data, key)
                filename = "encrypted_" + uploaded_file.filename
            elif action == "decrypt":
                result = aes_decrypt(file_data, key)
                filename = "decrypted_" + uploaded_file.filename
            else:
                return "❌ Hành động không hợp lệ", 400

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, "wb") as f:
                f.write(result)

            return render_template_string(template, filename=filename)

        except Exception as e:
            return f"❌ Lỗi xử lý: {str(e)}", 400

    return render_template_string(template, filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
