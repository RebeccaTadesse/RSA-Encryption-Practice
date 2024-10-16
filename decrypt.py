# decrypt.py
# Main code to decrypt text and video ciphertext files.

from crypto import decrypt_file, decrypt_pad

BLOCK_SIZE = 16             # characters per block

d = 458832241013449821620896012221731310864769306052555128482834043294065182867931498481836372851729623
n = 802956421773537187836568021388029794013346285592037135585214330086072630974836697183706878576307447

decrypt_file("ciphertext1.txt", "decrypted1.txt", d, n, BLOCK_SIZE)
print("Decrypted ciphertext1.txt")
decrypt_file("ciphertext2.txt", "decrypted2.txt", d, n, BLOCK_SIZE)
print("Decrypted ciphertext2.txt")

pad_file = open("pad.txt", "rb")
pad = decrypt_pad(pad_file, d, n, BLOCK_SIZE)
pad_file.close()
decrypt_file("encrypted-video", "decrypted-video.mp4", None, None, BLOCK_SIZE, pad)
print("Decrypted encrypted-video")

