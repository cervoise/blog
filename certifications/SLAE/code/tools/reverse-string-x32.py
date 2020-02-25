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
