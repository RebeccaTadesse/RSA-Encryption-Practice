# crypto.py
# Functions for CS 1 Lab Assignment 4.

from random import *

BYTE_SIZE = 8                   # bits per byte

# Return (x**d) % n.


def modular_exponentiation(x, d, n):
    if d == 0:
        return 1
    elif d % 2 == 0:
        y = modular_exponentiation(x, d // 2, n)
        return (y * y) % n
    else:
        return (modular_exponentiation(x, d-1, n) * x) % n

# Takes a bytes or bytearray object and converts it to an int.
# Character 0 of the bytes/bytearray should be in byte 0 (the rightmost
# byte) of the int when we are done.


def bytes_to_int(bytes):
    result = 0
    shift = 0

    for byte in bytes:
        result += byte << shift
        shift += BYTE_SIZE

    return result

# Takes an int x and converts it to a bytearray.  Byte 0 (the least significant
# byte of the int) becomes byte 0 of the bytearray.  Also takes as a parameter
# the number of bytes to include in the bytearray.


def int_to_bytes(x, size):
    result = bytearray()
    mask = 0xFF     # mask for isolating least significant byte

    for i in range(size):
        result.append(x & mask)
        x >>= BYTE_SIZE

    return result

# Generate a random pad for a given number of bytes.  Return the pad,
# represented as a bytearray.


def generate_pad(block_size):
    y = bytearray()
    for i in range(block_size):
        y.append(randint(0, 255))

    return y

# XOR a block of bytes, byte by byte, with a key, which is a bytearray.
# The key must be at least as long as the block.
# Return the XORed block of bytes as a bytearray.


def xor_block(key, block):
    # assert whether the length of the key is greater than that of the block
    assert len(key) >= len(block)

    # create an empty byte array
    x = bytearray()

    # append each XORed byte to the byte array
    for i in range(len(block)):
        x.append(block[i] ^ key[i])
    return x

# Encrypt a plaintext file into a ciphertext file, using the hybrid cryptosystem.
# Parameters are the name of the plaintext file, the name of the ciphertext file,
# the exponent and modulus used for RSA encryption of the one-time pad, the
# number of bytes in the one-time pad, and the one-time pad (if None, then generate
# the one-time pad).


def encrypt_file(plaintext_file_name, ciphertext_file_name, e, n, block_size, pad = None):
    plaintext = open(plaintext_file_name, 'rb')
    cipher = open(ciphertext_file_name, 'wb')

    if pad is None:
        pad = generate_pad(block_size)
        int_pad = bytes_to_int(pad)
        encrypted_pad = modular_exponentiation(int_pad, e, n)
        x = bytes(str(encrypted_pad) + '\n', "UTF-8")
        cipher.write(x)
    block = plaintext.read(block_size)
    while len(block) > 0:
        cipher.write(xor_block(pad, block))
        block = plaintext.read(block_size)
    plaintext.close()
    cipher.close()

# Decrypt just a one-time pad from a file.  Assumes that the file is already open and
# that the caller will close the file.  The encrypted one-time pad is text that is
# the first line in the file.  Parameters are the file object, the exponent and modulus
# used for RSA decryption of the one-time pad, and the number of bytes in the one-time
# pad.  Returns the one-time pad as a bytearray.


def decrypt_pad(pad_file, d, n, block_size):
    first_line = int(pad_file.readline())
    return int_to_bytes(modular_exponentiation(first_line, d, n), block_size)

# Decrypt a ciphertext file into a decrypted plaintext file, using the hybrid cryptosystem.
# Parameters are the name of the ciphertext file, the name of the decrypted plaintext file,
# the exponent and modulus used for RSA decryption of the one-time pad, the
# number of bytes in the one-time pad, and the one-time pad (if None, then read and
# decrypt the one-time pad from the ciphertext file).


def decrypt_file(ciphertext_file_name, decrypted_file_name, d, n, block_size, pad = None):
    cipher = open(ciphertext_file_name, 'rb')
    decrypt = open(decrypted_file_name, 'wb')
    if pad is None:
        pad = decrypt_pad(cipher, d, n, block_size)
    block = cipher.read(block_size)
    while len(block) > 0:
        decrypt.write(xor_block(pad, block))
        block = cipher.read(block_size)

    cipher.close()
    decrypt.close()
