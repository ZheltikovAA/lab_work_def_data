import random

def generate_gamma(length):
    """Генерация гаммы заданной длины."""
    res = [random.randint(0, 255) for _ in range(length)]
    print(res)
    return res

def substitution_encryption(password_string, key):
    """Шифрование заменой."""
    result = ""
    for element in password_string:
        if element.isalpha():
            first = ord('a') if element.islower() else ord('A')
            result += chr((ord(element) - first + key) % 26 + first)
        else:
            result += element  # Сохраняем неалфавитные символы
    return result

def gamma_encryption(substitution_encryption_string, gamma):
    """Шифрование гаммированием."""
    buffer_utf = substitution_encryption_string.encode('utf-8')
    return bytes([b ^ g for b, g in zip(buffer_utf, gamma)])

def substitution_decryption(encryption_string, key):
    """Дешифрование заменой."""
    result = ""
    for element in encryption_string:
        if element.isalpha():
            first = ord('a') if element.islower() else ord('A')
            result += chr((ord(element) - first - key) % 26 + first)
        else:
            result += element  # Сохраняем неалфавитные символы
    return result

def gamma_decryption(encryption_gamma_string, gamma):
    """Дешифрование гаммированием."""
    decrypted_bytes = bytes([b ^ g for b, g in zip(encryption_gamma_string, gamma)])
    return decrypted_bytes.decode('utf-8', errors='ignore')  # Игнорируем ошибки декодирования

def encrypt_password(password_string, key):
    """Шифрование пароля."""
    substitution_encrypted = substitution_encryption(password_string, key)
    gamma = generate_gamma(len(substitution_encrypted))  # Длина гаммы равна длине зашифрованной строки
    return gamma_encryption(substitution_encrypted, gamma), gamma

def decrypt_password(encryption_gamma_string, key, gamma):
    """Дешифрование пароля."""
    decrypted_substitution = gamma_decryption(encryption_gamma_string, gamma)
    return substitution_decryption(decrypted_substitution, key)