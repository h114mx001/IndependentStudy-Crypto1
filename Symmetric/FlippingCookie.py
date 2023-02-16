from Cryptodome.Cipher import AES
import requests
from pwn import xor

def get_cookie():
    url = "http://aes.cryptohack.org/flipping_cookie/get_cookie/"
    r = requests.get(url)
    js = r.json()
    return bytes.fromhex(js["cookie"])

def check_admin(cookie: bytes, iv: bytes):
    url = "http://aes.cryptohack.org/flipping_cookie/check_admin/"
    url += cookie.hex()
    url += "/"
    url += iv.hex()
    url += "/"
    r = requests.get(url)
    js = r.json()
    print(js)

cookie = get_cookie()
print(len(cookie)) # 48 => 3 block; with 1 iv and 2 cipher

iv = cookie[:16]
block1 = cookie[16:32]
block2 = cookie[32:]

get = b'admin=False;expi'
goal = b'admin=True;\x05\x05\x05\x05\x05'

send_iv = xor(xor(get, goal), iv)
check_admin(block1, send_iv)