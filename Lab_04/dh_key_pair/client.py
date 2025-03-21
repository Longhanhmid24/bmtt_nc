from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Hàm tạo cặp khóa Diffie-Hellman cho client
def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()  # Tạo khóa riêng
    public_key = private_key.public_key()  # Lấy khóa công khai từ khóa riêng
    return private_key, public_key

# Hàm tính toán khóa bí mật dùng Diffie-Hellman
def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)  # Trao đổi khóa
    return shared_key

def main():
    # Tải khóa công khai của server từ file
    with open("server_public_key.pem", "rb") as f:
        server_public_key = serialization.load_pem_public_key(f.read())

    # Lấy tham số từ khóa công khai của server
    parameters = server_public_key.parameters()

    # Tạo cặp khóa cho client
    private_key, public_key = generate_client_key_pair(parameters)

    # Tính khóa bí mật chung
    shared_secret = derive_shared_secret(private_key, server_public_key)

    print("Shared Secret:", shared_secret.hex())

# Kiểm tra nếu script được chạy trực tiếp
if __name__ == "__main__":
    main()
