import os
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

# Hàm tạo tham số Diffie-Hellman
def generate_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048)  # Tạo tham số DH
    return parameters

# Hàm tạo cặp khóa DH cho server
def generate_server_key_pair(parameters):
    private_key = parameters.generate_private_key()  
    public_key = private_key.public_key()  
    return private_key, public_key

def main():
    # Tạo thư mục nếu chưa tồn tại
    save_path = "week04/dh_key_pair"
    os.makedirs(save_path, exist_ok=True)

    # Tạo tham số DH
    parameters = generate_dh_parameters()

    # Tạo cặp khóa cho server
    private_key, public_key = generate_server_key_pair(parameters)

    # Lưu khóa công khai vào file
    public_key_path = os.path.join(save_path, "server_public_key.pem")
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    print(f"Khóa công khai đã được lưu vào: {public_key_path}")

# Kiểm tra nếu script được chạy trực tiếp
if __name__ == "__main__":
    main()
