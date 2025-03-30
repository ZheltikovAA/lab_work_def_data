import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Hash import MD2

DATABASE_FILENAME = 'example.db'
TEMP_DECRYPTED_FILE = 'temp_example.db'

# Параметры шифрования
KEY_SIZE = 16  # Для AES-128 требуется 16 байт
BLOCK_SIZE = AES.block_size

def hash_password(password):
    """Хэширует пароль используя MD2 для создания ключа"""
    hasher = MD2.new()
    hasher.update(password.encode())
    return hasher.digest()

def encrypt_file(input_filename, output_filename, password):
    """Шифрует файл с использованием AES-128 в режиме ECB"""
    key = hash_password(password)[:KEY_SIZE] if type(password) != bytes else password[:KEY_SIZE]
    cipher = AES.new(key, AES.MODE_ECB)

    with open(input_filename, 'rb') as f:
        data = f.read()

    # Добавляем padding для соответствия размеру блока
    pad_length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    data += bytes([pad_length]) * pad_length

    encrypted_data = cipher.encrypt(data)

    with open(output_filename, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(input_filename, output_filename, password):
    """Расшифровывает файл с использованием AES-128 в режиме ECB"""
    key = hash_password(password)[:KEY_SIZE] if type(password) != bytes else password[:KEY_SIZE]
    cipher = AES.new(key, AES.MODE_ECB)

    with open(input_filename, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = cipher.decrypt(encrypted_data)

    # Убираем padding
    pad_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad_length]

    with open(output_filename, 'wb') as f:
        f.write(decrypted_data)