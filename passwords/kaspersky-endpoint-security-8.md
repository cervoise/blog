Kaspersky Endpoint Security propose depuis un certain temps déjà, de restreindre certaines actions (désactivation de l’antivirus par exemple) via un mot de passe. De ce fait, les droits d’administration sur un poste ne permettent pas, en théorie, la maîtrise de l’antivirus.

Il est possible d’envisager une attaque par dictionnaire en utilisant un script simulant des entrées claviers (avec AutoIt ou bien Java Robot) ou bien de faire ça avec un Arduino Uno ou une Teensy. Bien sûr, il faut prendre une capture d’écran/photo à chaque tentative et les comparer manuellement ou bien avec ImageMagick ce qui reste assez fastidieux. Cependant, si l’utilisateur dispose des droits d’administration il est possible de d’accéder au registre et de le modifier et donc d’écraser le mot de passe comme indiqué sur le site suivant : www.fixkb.com/2009/06/how-to-remove-kaspersky-passwords.html.

En résumé cela consiste à modifier deux entrées dans le registre. Il faut aller dans la base de registre : 

```
HKEY_LOCAL_MACHINE\SOFTWARE\KasperskyLab\protected\AVP8\settings (32 bits)
HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\KasperskyLab\protected\AVP8\settings (64 bits)
```

Il faut modifier les entrées suivantes : 
```
EnablePswrdProtect -> 0
OPEP -> vide.
```

Ceci est aussi réalisable en montant le disque sur un autre système et permet de maîtriser sa solution antivirale ce qui est plus intéressant que de supprimer directement l’antivirus du disque, le tout à la main, ce qui reste plutôt malpropre.

A ce niveau, nous avons l’option attaque par dictionnaire assez lente, assez complexe à analyser ou bien la possibilité d’écraser le mot de passe. S’il est possible d’écraser le mot de passe, il est possible de tenter de le casser. Si l’on rentre password comme mot de passe on obtient l’entrée suivante : b081dbe85e1ec3ffc3d4e7d0227400cd. Cela ressemble à un MD5, cependant, le MD5 « classique » de password est 5f4dcc3b5aa765d61d8327deb882cf99. Il s’agit en fait du condensat MD5 au format unicode (https://www.freerainbowtables.com/phpBB3/viewtopic.php?f=2&t=256). Pour calculer le MD5 au format unicode (idem pour un SHA1) il suffit de rajouter un null byte avant (ou après dans le cas d’un unicode en big endian) comme c’est possible avec le code Python suivant :

```python
import hashlib
 
password = "password"
unipassword = ""
for letter in password:
    unipassword += letter + "\x00"
 
m = hashlib.md5()
m.update(unipassword)
print "Unicode: " + m.hexdigest()
 
n = hashlib.md5()
n.update(password)
print "Classic: " + n.hexdigest()
```
```
Unicode: b081dbe85e1ec3ffc3d4e7d0227400cd
Classic: 5f4dcc3b5aa765d61d8327deb882cf99
```
Pour attaquer ce type de mot de passe, on peut par exemple utiliser john avec le bon format :
```
john unicode-md5.txt --format=raw-md5u
```
