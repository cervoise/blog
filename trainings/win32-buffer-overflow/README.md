If you want to prepare yourself to a buffer overflow training (or certifications) or just learn, is there a list of exploit you can practices on. For each exploit I provide the type of exploitation and the target I used.

I recommend to start with these online ressources: 
 * fuzzysecurity: https://www.fuzzysecurity.com/tutorials.html
 * corelan: https://www.corelan.be/index.php/category/security/exploit-writing-tutorials/)
 * Windows shellcoding: http://www.vividmachines.com/shellcode/shellcode.html#ws

I did not crawl all possibilties of https://www.exploit-db.com, same program may be vulnerable in different ways. I can refer to the same exploit for different cases.

You can check for specific blog post:
  * https://www.offensive-security.com/vulndev/disarming-and-bypassing-emet-5-1/

## About security features

I am focusing on exploiting buffer overflows in order to gain code execution. If it is possible, I bypass some exploitation prevention such as ASLR or DEP. However, I am not digging in other security features bypass such as:
  * Windows firewall (but I may tell in the exploit file if it is possible to bypass it)
  * Antivirus bypass for the payload: pop a calc is enough
  * Applocker bypass: finding a way to bypass Applocker or finding an authorized program is another job
  
Regarding features that can prevent again execution:
  * ASLR is enable by default since Windows Vista.
  * DEP is configure by default for only be enable on specific compiled programs or libraries. DEP bypass for a programm that is not compiled with DEP is done on a Windows with PAE enable, on DEP enable for all programs. 

## Notes

For "old" systems, you may have trouble to find old tools:
 * OllyDbg200 (http://www.ollydbg.de/) is working on Windows 2000
 * OllyDbg110 (http://www.ollydbg.de/) is working on Windows 98 SE
 * arwin
   * can be compiled using *i686-w64-mingw32-gcc* on Linux
   * is not working on Windows 2000 (but you can check your DLL on another system)
  * WinDbg for Windows XP is available on the Waybackmachine: http://web.archive.org/web/20130118182453/https://msdl.microsoft.com/download/symbols/debuggers/dbg_x86_6.11.1.404.msi

Sometimes you have a both ASLR & DEP bypass, but the binary is too old for Windows Vista or newer. You can use:
  * EMET 4.1
    * You can find it on the Waybackmachine: https://web.archive.org/web/20140114083043/http://www.microsoft.com/en-us/download/details.aspx?id=41138
  * WehnTrust https://archive.codeplex.com/?p=wehntrust - In this case, you will have to:
    * install it
    * put an exception on your program

 
These exercices are also a good opportunity to test Metasploit payloads ;)

## Simple Win32 stack based buffer overflow

### Simple JMP ESP

 * BlazeDVD Pro Player 6.1 - https://www.exploit-db.com/exploits/26889 (Windows XP Pro SP3 FR)
   * There is a tutorial for exploiting this software in the [Exploiting Simple Buffer Overflows on Win32](https://www.pentesteracademy.com/course?id=13) (not free).
 * MiniShare 1.4.1 - https://www.exploit-db.com/exploits/616   (Windows XP Pro SP3 FR)
   * There is a tutorial for exploiting this software in the [Exploiting Simple Buffer Overflows on Win32](https://www.pentesteracademy.com/course?id=13) (not free).
 * WarFTP 1.65 - https://www.exploit-db.com/exploits/3570  (Windows XP Pro SP3 FR)
   * There is a tutorial for exploiting this software in the [Exploiting Simple Buffer Overflows on Win32](https://www.pentesteracademy.com/course?id=13) (not free).
 * freeSSHd 1.0.9 - https://www.exploit-db.com/exploits/1787  (Windows XP Pro SP3 FR)
   * There is a tutorial for exploiting this software in the [Exploiting Simple Buffer Overflows on Win32](https://www.pentesteracademy.com/course?id=13) (not free).
 * Easy RM to MP3 Converter 2.7.3.700 - https://www.exploit-db.com/exploits/10374 (Windows XP Pro SP3 FR)
   * There is a tutorial in [fuzzysecurity](https://www.fuzzysecurity.com/tutorials/expDev/6.html) for DEP bypass.
 * Freefloat FTP Server - https://www.exploit-db.com/exploits/23243 (Windows XP Pro SP3 FR)
   * Similar vulnerabilities in the same program: https://www.exploit-db.com/exploits/17539, https://www.exploit-db.com/exploits/40673 (https://www.exploit-db.com/search?q=freefloat).
   * There is a tutorial in [fuzzysecurity](https://www.fuzzysecurity.com/tutorials/expDev/2.html)
   * DEP bypass exists: https://www.exploit-db.com/exploits/17886 (Windows XP Pro SP3 FR)
 * Ollydbg 2.00 Beta1 - https://www.exploit-db.com/exploits/11465 (Windows XP Pro SP3 FR)
 * AtomixMP3 < 2.3 - https://www.exploit-db.com/exploits/2873  (Windows XP Pro SP3 FR)
 * XMPlay 3.3.0.4- https://www.exploit-db.com/exploits/2824  (Windows XP Pro SP3 FR)
   * Similar vulnerabilities in the same program: https://www.exploit-db.com/exploits/2815 - https://www.exploit-db.com/exploits/2821
 * CesarFTP 0.99g - https://www.exploit-db.com/exploits/1906  (Windows XP Pro SP3 FR)
 * Aviosoft Digital TV Player Professional 1.x - https://www.exploit-db.com/exploits/22932 (Windows XP Pro SP3 FR)
   * There is a tutorial for exploiting this software in the [Exploiting Simple Buffer Overflows on Win32](https://www.pentesteracademy.com/course?id=13) (not free).
 * MicroP 0.1.1.1600 - https://www.exploit-db.com/exploits/14720 (Windows XP Pro SP3 FR)
   * There is a tutorial for exploiting this software in the [Exploiting Simple Buffer Overflows on Win32](https://www.pentesteracademy.com/course?id=13) (not free).

### Small space - Write your shellcode

 * WinRAR 1.0 - https://www.exploit-db.com/exploits/558   (Windows 2000 Pro RC2 FR)
 * Kolibri Web Server 2.0 - https://www.exploit-db.com/exploits/33027 (Windows XP Pro SP3 FR)
 * mIRC 6.1 - https://www.exploit-db.com/exploits/112   (Windows XP Pro SP3 FR)

### Small space - Egghunter

 * Kolibri Web Server 2.0 - https://www.exploit-db.com/exploits/33027 (Windows XP Pro SP3 FR)
    * There is a tutorial in [fuzzysecurity](https://www.fuzzysecurity.com/tutorials/expDev/3.html).
 * Winamp 5.12 - https://www.exploit-db.com/exploits/3422
   * This one is tricky and have small space you can:
      * use a short homemade shellcode (Windows XP Pro SP3 FR),
      * play with ESP to find more space (Windows XP Pro SP3 FR / Windows 7 Pro SP1 EN)
      * or use an egghunter (Windows XP Pro SP3 FR).
   * Two other version of this exploit are available: https://www.exploit-db.com/exploits/1458 and https://www.exploit-db.com/exploits/1460
   * This software is vulnerable to the same injection for another file type: https://www.exploit-db.com/exploits/26245

## Tricky Win32 stack based buffer overflow

 * MS07-017 on Internet Explorer for Windows XP - https://www.exploit-db.com/exploits/16526
   * You can find a vulnerable IE version on Windows XP NO SP/SP1/SP2
 * MS00-005 - https://www.exploit-db.com/exploits/19633
   * You can find a vulnerable WordPad on Windows 98 SE
 * Winamp 5.12 - https://www.exploit-db.com/exploits/3422 
   * This one is tricky and have small space you can:
      * use a short homemade shellcode (Windows XP Pro SP3 FR),
      * play with ESP to find more space (Windows XP Pro SP3 FR / Windows 7 Pro SP1 EN)
      * or use an egghunter (Windows XP Pro SP3 FR).
   * Two other version of this exploit are available: https://www.exploit-db.com/exploits/1458 and https://www.exploit-db.com/exploits/1460
   * This software is vulnerable to the same injection for another file type: https://www.exploit-db.com/exploits/26245
   
## Win32 Stack based buffer overflow with SEH

 * DVD X Player 5.5 Pro - https://www.exploit-db.com/exploits/17788 (Windows XP Pro SP3 FR)
   * There is a tutorial in [fuzzysecurity](https://www.fuzzysecurity.com/tutorials/expDev/3.html).
 * R 3.4.4 - https://www.exploit-db.com/exploits/45289 (Windows XP Pro SP3 FR)
 
### 3-bytes overwrite with egghunter
 * Nsauditor 3.0.28.0 - https://www.exploit-db.com/exploits/46005 (Windows XP Pro SP3 FR)
  * Nsauditor 3.2.1.0 is still vulnerable
  * This should bypass ASLR if the egghunter was working on newer Windows versions.
  * An exploit without egghunter is possible, I've done one that works for both Nsauditor 3.0.28.0/3.2.1.0 https://www.exploit-db.com/exploits/48350 (Windows XP Pro SP3 FR / Windows 10.0.18363.778 Pro EN)

 
## Win32 Stack based buffer overflow - DEP bypass

Note: Once you have your ROP chain bypass for a system, you can reuse it for many software.

### SetProcessDEPPolicy

  * Freefloat FTP Server - https://www.exploit-db.com/exploits/23243 (Windows XP Pro SP3 FR)
    * Similar vulnerabilities in the same program: https://www.exploit-db.com/exploits/17539, https://www.exploit-db.com/exploits/40673 (https://www.exploit-db.com/search?q=freefloat).
    * There is a tutorial in [fuzzysecurity](https://www.fuzzysecurity.com/tutorials/expDev/2.html)
    * DEP bypass exists: https://www.exploit-db.com/exploits/17886 (Windows XP Pro SP3 FR)
  * WarFTP 1.65 - https://www.exploit-db.com/exploits/3570  (Windows XP Pro SP3 FR)
 
 ## Win32 Stack based buffer overflow - ASLR bypass
 ### Non-ASLR enabled module (JMP ESP or equivalent)
  * Socusoft Photo to Video Converter 8.07 - https://www.exploit-db.com/exploits/45406 (Windows 7 Pro SP1 EN, also work on Windows XP Pro SP3 FR (no ASLR))
  * VUPlayer 2.44 - https://www.exploit-db.com/exploits/2870 (Windows 7 Pro SP1 EN, also work on Windows XP Pro SP3 FR (no ASLR))
  #### Tricky
   * FTP Commander Pro 8.03 - https://www.exploit-db.com/exploits/47775 (Windows 10.0.18363.778 Pro EN)
   * Winamp 5.12 - https://www.exploit-db.com/exploits/3422 
     * This one is tricky and have small space you can:
      * play with ESP to find more space (Windows XP Pro SP3 FR (no ASLR) / Windows 7 Pro SP1 EN).
 ### Non-ASLR enabled module with SEH
  * Boxoft WAV to MP3 Converter 1.1 - https://www.exploit-db.com/exploits/44971 (Windows 7 Pro SP1 EN / XP Pro SP3 FR (no ASLR))
  * Allok Quicktime to AVI MPEG DVD Converter 4.6.1217 - https://www.exploit-db.com/exploits/44330 (Windows 7 Pro SP1 EN / XP Pro SP3 FR (no ASLR))
  * DVD X Player 5.5 Pro - https://www.exploit-db.com/exploits/17788 (Windows 10.0.18363.778 Pro EN)

#### 3-bytes overwrite with egghunte
 * Nsauditor 3.0.28.0 - https://www.exploit-db.com/exploits/48350 (Windows XP Pro SP3 FR / Windows 10.0.18363.778 Pro EN)
  * Nsauditor 3.2.1.0 is still vulnerable

### Non-ASLR enabled module with SEH - Unicode
  * Triologic Media Player 8 - https://www.exploit-db.com/exploits/14673 (Windows 10.0.18363.778 Pro EN / Windows XP Pro SP3 FR (no ASLR))
    * There is a tutorial on [fuzzysecurity](https://www.fuzzysecurity.com/tutorials/expDev/5.html).

 ### Partial EIP overwrite
  * MS07-017 on Internet Explorer for Windows Vista - https://www.exploit-db.com/exploits/16526
    * You can find a vulnerable IE version on Windows Vista NO SP

## Win32 Stack based buffer overflow - DEP & ASLR bypass

### SetProcessDEPPolicy
  * WarFTP 1.65 - https://www.exploit-db.com/exploits/3570  (Windows XP Pro SP3 FR with WehnTrust 1.2)
