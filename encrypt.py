# encrypt.py
# Main code to encrypt a plaintext file.

from crypto import encrypt_file
BLOCK_SIZE = 16

e = 7
n = 863559414525978737163425621330572722678614948064538867862514518404465002065904353361531101863861367

encrypt_file("decrypted2.txt", "ciphertext.txt", e, n, BLOCK_SIZE, None)