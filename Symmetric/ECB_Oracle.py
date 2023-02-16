import requests
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

flag = b"crypto{"

# flag length is 26

def response(byte_string):
	url = "http://aes.cryptohack.org/ecb_oracle/encrypt/"
	url += byte_string.hex()
	url += "/"
	r = requests.get(url)
	js = r.json()
	return bytes.fromhex(js["ciphertext"])

for i in range(7, 26):
	byte_string = b""
	byte_string += b"\x00" * (31 - i)
	
	res = response(byte_string)[:32]

	byte_string += flag
	for j in range(33, 128):
		byte_string = byte_string[:31]
		byte_string += j.to_bytes(1, byteorder = "big")
		print(j)

		res2 = response(byte_string)[:32]
		if res == res2:
			flag += j.to_bytes(1, byteorder = "big")
			print(flag)
			break