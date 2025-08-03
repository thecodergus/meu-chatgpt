import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Carrega chave mestre de criptografia do ambiente (base64 32 bytes)
MASTER_KEY_B64 = os.getenv("CRYPTO_MASTER_KEY")
if not MASTER_KEY_B64:
    raise ValueError("CRYPTO_MASTER_KEY não encontrada no ambiente")
MASTER_KEY = base64.b64decode(MASTER_KEY_B64)
if len(MASTER_KEY) != 32:
    raise ValueError("CRYPTO_MASTER_KEY deve ser uma chave base64 de 32 bytes")

aesgcm = AESGCM(MASTER_KEY)

def encrypt(data: bytes) -> bytes:
    """Criptografa bytes retornando nonce + ciphertext"""
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return nonce + ct

def decrypt(token: bytes) -> bytes:
    """Descriptografa nonce + ciphertext retornando bytes originais"""
    nonce = token[:12]
    ct = token[12:]
    return aesgcm.decrypt(nonce, ct, None)

def encrypt_str(text: str) -> bytes:
    """Criptografa string UTF-8 retornando bytes criptografados"""
    return encrypt(text.encode("utf-8"))

def decrypt_str(token: bytes) -> str:
    """Descriptografa bytes retornando string UTF-8"""
    return decrypt(token).decode("utf-8")