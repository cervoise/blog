If you want to prepare yourself to a buffer overflow training (or certifications) or just learn, is there a list of exploit you can practices on. For each exploit I provide the type of exploitation and the target I used.

I recommend to start with these online ressources: 
 * fuzzysecurity: https://www.fuzzysecurity.com/tutorials.html
 * corelan: https://www.corelan.be/index.php/category/security/exploit-writing-tutorials/)
 * Windows shellcoding: http://www.vividmachines.com/shellcode/shellcode.html#ws

## Notes

For "old" systems, you may have trouble to find old tools:
 * OllyDbg200 (http://www.ollydbg.de/) is working on Windows 2000
 * arwin
   * can be compiled using *i686-w64-mingw32-gcc* on Linux
   * is not working on Windows 2000 (but you can check your DLL on another sytem)
  * WinDbg for Windows XP is available on the Waybackmachine: http://web.archive.org/web/20130118182453/https://msdl.microsoft.com/download/symbols/debuggers/dbg_x86_6.11.1.404.msi

## Simple Win32 stack based buffer overflow

### Simple JMP ESP

 * https://www.exploit-db.com/exploits/26889 (Windows XP Pro SP3 FR)
 * https://www.exploit-db.com/exploits/616 (Windows XP Pro SP3 FR)
 * https://www.exploit-db.com/exploits/3570 (Windows XP Pro SP3 FR)
 * https://www.exploit-db.com/exploits/1787 (Windows XP Pro SP3 FR)
 * https://www.exploit-db.com/exploits/1906 (Windows XP Pro SP3 FR)
 * https://www.exploit-db.com/exploits/10374 (Windows XP Pro SP3 FR)
 * https://www.exploit-db.com/exploits/23243 (Windows XP Pro SP3 FR)

### Small space - Write your shellcode

 * https://www.exploit-db.com/exploits/558 (Windows 2000 Pro RC2 FR)

## Tricky Win32 stack based buffer overflow

 * MS07-017 on Internet Explorer for Windows XP (you can find a vulnerable IE version on Windows XP SP1)

## Win32 Stack based buffer overflow with SEH

 * https://www.exploit-db.com/exploits/17788 (Windows XP Pro SP3 FR)
 * https://www.exploit-db.com/exploits/45289 (Windows XP Pro SP3 FR)
