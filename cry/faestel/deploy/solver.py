from pwn import *
import sys
from cipher import Faestel, xor
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BINARY_PATH = './prob.py'
if len(sys.argv) == 3:
    p = remote(sys.argv[1], int(sys.argv[2]))
else:
    p = process(BINARY_PATH)

PAD0 = pad(b'\x00', 14)
PAD1 = pad(b'\x01', 14)
PAD2 = pad(b'\x02', 14)

def faestel_enc(pt: bytes) -> bytes:
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'plaintext(hex)> ', pt.hex().encode())
    p.recvuntil(b'ciphertext(hex)> ')
    ct = p.recvline(keepends=False).decode()
    return bytes.fromhex(ct)

def aes_enc(key: bytes, pt: bytes) -> bytes:
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(pt)

def getflag() -> bytes:
    p.sendlineafter(b'> ', b'2')
    p.recvuntil(b'encrypted flag(hex)> ')
    enc_flag = p.recvline(keepends=False).decode()
    return bytes.fromhex(enc_flag)

pt = b'0'*32
ct = faestel_enc(pt)
enc_flag = getflag()

x = pt[ 0:16]
y = pt[16:32]
u = ct[ 0:16]
v = ct[16:32]

print(f'{x.hex() = }')
print(f'{y.hex() = }')
print(f'{u.hex() = }')
print(f'{v.hex() = }')

# key: z, value: corresponding first round key
z_dict: dict[bytes, bytes] = {}
for i in range(0x10000):
    tmpk1 = int.to_bytes(i, 2, byteorder='big') + PAD0
    tmpz = xor(aes_enc(tmpk1, y), x)
    z_dict[tmpz] = tmpk1

for i in range(0x10000):
    tmpk3 = int.to_bytes(i, 2, byteorder='big') + PAD2
    tmpz = xor(aes_enc(tmpk3, v), u)
    if tmpz in z_dict:
        z = tmpz
        k1 = z_dict[z]
        k3 = tmpk3
        break

enc_z = xor(v,y)
for i in range(0x10000):
    tmpk2 = int.to_bytes(i, 2, 'big') + PAD1
    if aes_enc(tmpk2, z) == enc_z:
        k2 = tmpk2
        break

print(f'{z.hex() = }')
print(f'{k1.hex() = }')
print(f'{k2.hex() = }')
print(f'{k3.hex() = }')

# validation
v_pt = b'1'*32
v_ct = faestel_enc(v_pt)
master_key = k1[:2]+k2[:2]+k3[:2]
recovered_faestel = Faestel(master_key)
assert v_ct == recovered_faestel.encrypt(v_pt)

newkey = xor(master_key, b'faeste')
newfaestel = Faestel(newkey)
flag = newfaestel.decrypt(enc_flag)
print(flag)
