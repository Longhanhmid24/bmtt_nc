import ecdsa
import os

class ECCCipher:
    def __init__(self):
        pass

    def generate_keys(self):
        sk = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        vk = sk.get_verifying_key()

        key_dir = 'cipher/ecc/keys/'
        if not os.path.exists(key_dir):
            os.makedirs(key_dir)

        with open(os.path.join(key_dir, 'privateKey.pem'), 'wb') as p:
            p.write(sk.to_pem())

        with open(os.path.join(key_dir, 'publicKey.pem'), 'wb') as p:
            p.write(vk.to_pem())

        print("Khóa đã được tạo thành công!")

    def load_keys(self):
        with open('cipher/ecc/keys/privateKey.pem', 'rb') as p:
            sk = ecdsa.SigningKey.from_pem(p.read())

        with open('cipher/ecc/keys/publicKey.pem', 'rb') as p:
            vk = ecdsa.VerifyingKey.from_pem(p.read())

        return sk, vk  # sk là SigningKey, vk là VerifyingKey

    def sign(self, message, sk):
        return sk.sign(message.encode('ascii'))

    def verify(self, message, signature, vk):
        try:
            return vk.verify(signature, message.encode('ascii'))  # Đảm bảo vk là VerifyingKey
        except ecdsa.BadSignatureError:
            return False

