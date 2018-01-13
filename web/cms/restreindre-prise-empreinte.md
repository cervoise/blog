# « Empêcher » la prise d’empreinte d’applications Web

Publication : 4 octobre 2012

Un moyen envisageable de se protéger contre ce type d’outil consisterai à ajouter du sel dans les fichiers via une chaîne de caractères aléatoires en commentaire. Cela se script d’ailleurs assez bien, voici un exemple qui rajoute ce sel aux fichiers HTM/HTML, CSS et JS. Il suffit de rentrer l’adresse du répertoire racine de votre CMS sur votre disque et de lancer le script.

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import os
import string
import random
 
def listdirectory(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for i in files:
            file_list.append(os.path.join(root, i))
 
    return file_list
 
def get_a_random_string(size):
    random_string = ""
    for i in range(size):
        random_string += random.choice(string.letters)
 
    return random_string
 
cms_folder = "/CMS/ROOT/FOLDER/"
 
for ffile in listdirectory(cms_folder):
    print ffile
    if ffile[-5:] == ".html" or ffile[-4:] == ".htm":
        f = open(ffile, 'a+')
        f.write('\n<!--' + get_a_random_string(15) + '-->\n')
        f.close()
    elif ffile[-4:] == ".css" or ffile[-3:] == ".js":
        f = open(ffile, 'a+')
        f.write('\n/*' + get_a_random_string(15) + '*/\n')
        f.close()
```

Il s’agit plus d’un moyen de rendre cette prise d’empreinte plus difficile. En effet, l’ « attaquant » peut utiliser d’autres ressources comme les fichiers images ou encore télécharger les fichiers un à un et supprimer le sel.
