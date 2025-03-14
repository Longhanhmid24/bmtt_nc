from flask import Flask, request, jsonify
from cipher.rsa.rsa_algothm import RSACipher
from cipher.ecc.ecc_cipher import ECCCipher

app = Flask(__name__)

# Khởi tạo các đối tượng mã hóa
rsa_cipher = RSACipher()
ecc_cipher = ECCCipher()

# ------------------- RSA CIPHER -------------------

@app.route('/api/rsa/generate_keys', methods=['GET'])
def rsa_generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'RSA keys generated successfully'})

@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    data = request.json
    message = data.get('plain_text', '')
    key_type = data.get('key_type', '')

    private_key, public_key = rsa_cipher.load_keys()
    key = public_key if key_type == 'public' else private_key if key_type == 'private' else None

    if key is None:
        return jsonify({'error': 'Invalid key_type, must be "public" or "private"'}), 400

    encrypted_message = rsa_cipher.encrypt(message, key)
    return jsonify({'encrypted_message': encrypted_message.hex()})

@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    data = request.json
    cipher_text_hex = data.get('cipher_text', '')
    key_type = data.get('key_type', '')

    try:
        cipher_text = bytes.fromhex(cipher_text_hex)
    except ValueError:
        return jsonify({'error': 'Invalid cipher_text format, must be hex'}), 400

    private_key, public_key = rsa_cipher.load_keys()
    key = private_key if key_type == 'private' else None

    if key is None:
        return jsonify({'error': 'Invalid key_type, must be "private"'}), 400

    decrypted_message = rsa_cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_message})

@app.route('/api/rsa/sign', methods=['POST'])
def rsa_sign_message():
    data = request.json
    message = data.get('message', '')
    private_key, _ = rsa_cipher.load_keys()

    signature = rsa_cipher.sign(message, private_key)
    return jsonify({'signature': signature.hex()})

@app.route('/api/rsa/verify', methods=['POST'])
def rsa_verify_signature():
    data = request.json
    message = data.get('message', '')
    signature_hex = data.get('signature', '')

    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return jsonify({'error': 'Invalid signature format, must be hex'}), 400

    public_key, _ = rsa_cipher.load_keys()
    is_verified = rsa_cipher.verify(message, signature, public_key)

    return jsonify({'is_verified': is_verified})

# ------------------- ECC CIPHER -------------------

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'ECC keys generated successfully'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data.get('message', '')
    private_key, _ = ecc_cipher.load_keys()
    
    signature = ecc_cipher.sign(message, private_key)
    return jsonify({'signature': signature.hex()})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_message():
    data = request.json
    message = data.get('message', '')
    signature_hex = data.get('signature', '')

    try:
        signature = bytes.fromhex(signature_hex)
    except ValueError:
        return jsonify({'error': 'Invalid signature format, must be hex'}), 400

    _, vk = ecc_cipher.load_keys()
    is_verified = ecc_cipher.verify(message, signature, vk)

    return jsonify({'is_verified': is_verified})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
