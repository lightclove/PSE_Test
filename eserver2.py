from random import Random
from socket import socket

import RSA as RSA

try:
    # setting up socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
except BaseException:
    print
"-----Check Server Address or Port-----"
random_generator = Random.new().read
key = RSA.generate(1024, random_generator)
public = key.publickey().exportKey()
hash_object = hashlib.sha1(public)
hex_digest = hash_object.hexdigest()
# encrypt CTR MODE session key
en = AES.new(key_128, AES.MODE_CTR, counter=lambda: key_128)
encrypto = en.encrypt(key_128)
# hashing sha1
en_object = hashlib.sha1(encrypto)
en_digest = en_object.hexdigest()
# encrypting session key and public key
E = server_public_key.encrypt(encrypto, 16)
ideaEncrypt = IDEA.new(key, IDEA.MODE_CTR, counter=lambda: key)
eMsg = ideaEncrypt.encrypt(whole)
# converting the encrypted message to HEXADECIMAL to readable eMsg =
eMsg.encode("hex").upper()
decoded = newmess.decode("hex")
ideaDecrypt = IDEA.new(key, IDEA.MODE_CTR, counter=lambda: key)
dMsg = ideaDecrypt.decrypt(decoded)
