Check the file's protection

![checksec](https://github.com/OceanTran999/THM-PWN101/assets/100577019/76ac4c9e-8c0f-4eb2-b159-8da54acfcaa2)


Here're the `main()` function and `holidays()` function, we can see that this is the `ret2win` challenge.

![main](https://github.com/OceanTran999/THM-PWN101/assets/100577019/322257e6-29cc-4535-9736-4ca1b05a8f6d)


![holidays](https://github.com/OceanTran999/THM-PWN101/assets/100577019/a2da49fd-cea5-4a5e-97f2-4e8e0a83f13b)


There're 2 vulnerabilities in this challenge, the first is the format string vulnerability in `line 20` and the second is the buffer overflow in `line 16`. Running the program we can see that our first input is at 10th position in the stack.

![run1](https://github.com/OceanTran999/THM-PWN101/assets/100577019/c788daaf-2feb-45d0-8e9d-4dd219430a4f)

Due to the protection of program has `Partial RELRO`, we can overwrite the Global Offset Table (GOT) function to manipulate the program to call other function such as `system()` although we call `printf()` or `puts()` functions. For example, looking at `holidays` function, we see that the function has `<printf@plt>` and `<system@plt>`, when the program call these functions, they will find these function in the GOT. If the function is not available, the program will call it through local library such as `LIBC` and update the GOT for the next call. Therefore if we overwrite the GOT of `<printf@plt>` to the `system()` function, the program will run `system()` instead of `printf()`.

![disas_holidays](https://github.com/OceanTran999/THM-PWN101/assets/100577019/e2eb47ce-c6f2-4428-bb16-4850bd7a22e2)


To overwrite the value in the stack, we use `%n` to write the value in the specific position in the stack. The syntax will be: `%(value + format string)%(position)%n + padding`. Let's give an example, now I want to change the GOT of `puts()` function to 0x40, my payload will be like this:

![code](https://github.com/OceanTran999/THM-PWN101/assets/100577019/5769d035-cdfe-4781-89de-dabdbb0a39aa)


As the position of payload is started at 10th, the vulnerable program is 64-bit and the length of `%40x%12$n` is 9, so will need more 7 bytes to fill full the stack frame so that we can add the address of the GOT `puts()` in the next 8 bytes which is at 12th in the stack. To make sure if we successfully overwrite it, I use `radare2` to check:

![sym imp printf](https://github.com/OceanTran999/THM-PWN101/assets/100577019/a5a10c3c-32e1-42fb-b425-4a983ac802a1)


![reloc_puts2](https://github.com/OceanTran999/THM-PWN101/assets/100577019/8ce3537f-e813-4111-8bd4-deeb8a0d0a0c)


![reloc_puts3](https://github.com/OceanTran999/THM-PWN101/assets/100577019/167f1eae-8902-419d-bc9c-0e7b8705a540)

As you can see, the first byte address of GOT `puts()` function is `7f9a...5b00`, but after we input the format string vulnerability, overwriting 4 bytes to this address, the GOT `puts()` function is modified to `7f9a00...28` which is `0x28 = 40`. With this, we will overwrite the GOT `puts()` function and point it to the `holidays()` function to get the shell.

![code2](https://github.com/OceanTran999/THM-PWN101/assets/100577019/ad6315cc-1205-49a2-a064-325bd19a9f95)


![reloc_puts4](https://github.com/OceanTran999/THM-PWN101/assets/100577019/26cbd6cc-efc7-4a78-b61d-fe2d68581c25)


And don't forget to remove the first 2 byte `0x7f39` to call the `holidays()` function

![cod3](https://github.com/OceanTran999/THM-PWN101/assets/100577019/2647c279-85ed-4eb5-b8f0-007ef88e7270)


![reloc_puts5](https://github.com/OceanTran999/THM-PWN101/assets/100577019/ab5e083e-0475-4bed-883b-0dba074dd894)


![flag](https://github.com/OceanTran999/THM-PWN101/assets/100577019/b25613e4-b58c-448a-8c49-5b920c1101ad)
