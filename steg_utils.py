import os
import base64
import hashlib
from PIL import Image
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
END_MARK = "####END####"
EOF_MARK = b"STEGO_END::"
def get_sha256_key(password):
    return hashlib.sha256(password.encode("utf-8")).digest()
def generate_unique_key_pair(password):
    key = RSA.generate(2048)
    password_hash = get_sha256_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(password_hash, AES.MODE_CBC, iv)
    encrypted_priv = iv + cipher.encrypt(pad(key.export_key(), AES.block_size))
    return key.public_key(), encrypted_priv

def run_hybrid_encryption(message, image_password, private_key_password):
    pub_key, encrypted_priv = generate_unique_key_pair(private_key_password)
    
    aes_key = hashlib.sha256(image_password.encode()).digest()
    iv = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    
    encrypted_msg = base64.b64encode(iv + cipher_aes.encrypt(pad(message.encode(), AES.block_size)))
    encrypted_aes_key = base64.b64encode(PKCS1_OAEP.new(pub_key).encrypt(aes_key))
    return f"{base64.b64encode(encrypted_priv).decode()}|||{encrypted_aes_key.decode()}|||{encrypted_msg.decode()}"

def run_hybrid_decryption(combined_string, image_password, private_key_password):
    # 1. Unpack the components
    enc_priv_b64, enc_key_b64, enc_msg_b64 = combined_string.split("|||", 2)
    
    # 2. Decrypt the Private Key
    enc_priv_data = base64.b64decode(enc_priv_b64)
    cipher = AES.new(get_sha256_key(private_key_password), AES.MODE_CBC, enc_priv_data[:16])
    priv_key = RSA.import_key(unpad(cipher.decrypt(enc_priv_data[16:]), AES.block_size))
    aes_key = PKCS1_OAEP.new(priv_key).decrypt(base64.b64decode(enc_key_b64))
    enc_msg_data = base64.b64decode(enc_msg_b64)
    iv = enc_msg_data[:16]
    encrypted_payload = enc_msg_data[16:]
    
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_msg = unpad(cipher_aes.decrypt(encrypted_payload), AES.block_size)
    return decrypted_msg.decode('utf-8')
def hide_in_image(src, dest, secret, image_password, private_key_password):
    payload = run_hybrid_encryption(secret, image_password, private_key_password) + END_MARK
    img = Image.open(src).convert("RGB")
    bits = ''.join(format(ord(ch), '08b') for ch in payload)
    pixels = list(img.getdata())
    if len(bits) > len(pixels) * 3: raise ValueError("Payload too large!")
    new_pixels = []
    bit_idx = 0
    for p in pixels:
        new_p = list(p)
        for i in range(3):
            if bit_idx < len(bits):
                new_p[i] = (new_p[i] & ~1) | int(bits[bit_idx])
                bit_idx += 1
        new_pixels.append(tuple(new_p))
    img.putdata(new_pixels)
    img.save(dest, "PNG")
def hide_in_file_eof(src, dest, secret,  image_password, private_key_password):
    payload = EOF_MARK + run_hybrid_encryption(secret, image_password, private_key_password).encode()
    with open(src, "rb") as f: data = f.read()
    with open(dest, "wb") as f: f.write(data + payload)
def extract_from_any(file_path, image_password, private_key_password):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".png", ".jpg", ".jpeg", ".bmp"]:
        img = Image.open(file_path).convert("RGB")
        bits = "".join([str(c & 1) for p in list(img.getdata()) for c in p])
        chars = "".join([chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)])
        return run_hybrid_decryption(chars.split(END_MARK)[0], image_password,private_key_password)
    else:
        with open(file_path, "rb") as f: data = f.read()
        payload = data.rsplit(EOF_MARK, 1)[1].decode()
        return run_hybrid_decryption(payload, image_password, private_key_password)