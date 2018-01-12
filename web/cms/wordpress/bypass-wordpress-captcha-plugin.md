# Contournement du plugin Captcha pour WordPress v. 3.8.1 et antérieures
Publication : 27 mars 2014

Lorsque je tombe sur un captcha, j’aime bien regarder s’il celui-ci n’est pas cassable simplement en exploitant une erreur d’implémentation. Je m’étais ainsi rendu compte que [le plugin Captcha](https://wordpress.org/plugins/captcha/) pour WordPress avait l’un de ces défauts.

Le plugin Captcha, est un plugin permettant l’ajout d’un captcha à différentes interfaces de WordPress (page de login, publication de commentaires, etc.). La forme du captcha est une opération mathématique à résoudre.

![Plugin Captcha](http://www.antoine-cervoise.fr/wp-content/uploads/2014/03/login.jpg)

S’agissant d’une opération à résoudre, on peut envisager la création d’un script résolvant tout seul l’opération. Cependant, la case à remplir n’est pas fixe et les nombres peuvent être écrit en chiffres ou en lettres.

![Example 1](http://www.antoine-cervoise.fr/wp-content/uploads/2014/03/captcha3.jpg)
![Example 2](http://www.antoine-cervoise.fr/wp-content/uploads/2014/03/captcha1.jpg)
![Example 3](http://www.antoine-cervoise.fr/wp-content/uploads/2014/03/captcha2.jpg)

La mise en place d’un tel outil peut donc être fastidieuse. Par contre si l’on regarde dans le code source de la page, on découvre la présence d’un input HTML de type *hidden*.

![HTML hidden code](http://www.antoine-cervoise.fr/wp-content/uploads/2014/03/code_html.jpg)

En cherchant dans le code source de l’application on découvre une fonction decode, qui permet de déterminer le résultat attendu via cette chaine. Afin de complexifier l’attaque de cette chaine, la fonction utilise une clé et du sel. Au cours de mes premières recherches, je me suis rendu compte que la clé et le sel étaient fixés de manière statique (en dur dans le code) et ne changeaient pas entre chaque version.

![Key 1](http://www.antoine-cervoise.fr/wp-content/uploads/2014/03/str_key_old.jpg)
![Decode function 2](http://www.antoine-cervoise.fr/wp-content/uploads/2014/03/decode_old.jpg)

J’ai donc réalisé un petit script PHP permettant de casser le captcha (jusqu’en version 2.24). Vous trouverez le script [ici](https://github.com/cervoise/pentest-scripts/blob/master/web/cms/captcha-bypass/wordpress-plugins/captcha/bypass-2.34-previous.php). Comme précisé, ce script fonctionne jusqu’en version 2.34. En effet à partir de la version 2.4 et jusqu’à la version 3.8.1 l’éditeur a commencé à changer régulièrement la clé et le sel. Depuis la version 3.8.2, l’application utilise du sel dynamiquement généré ne permettant plus de deviner simplement la réponse du captcha via le champ *hidden*.

```
= V3.8.2 - 23.09.2013 =
* Bugfix : Captcha protection is improved by changing hidden values in every session.
```
![Key 2](http://www.cervezhack.fr/wp-content/uploads/2014/03/str_key_new-300x66.jpg)
![Decode function 2](http://www.cervezhack.fr/wp-content/uploads/2014/03/decode_new-300x166.jpg)

J’ai alors décidé de récupérer un maximum de versions vulnérables afin de réaliser un tableau des clés et du sel en fonction des versions. Pour cela j’ai réalisé un script qui récupère les versions dans le [changelog](http://wordpress.org/plugins/captcha/changelog/), les télécharge sur le site de wordpress (en effet, wordpress.org semble conserver les anciennes versions des plugins). Je récupère alors la clé et le sel dans chaque archive zip de chaque version vulnérable. Le script est disponible [ici](https://github.com/cervoise/pentest-scripts/blob/master/web/cms/captcha-bypass/wordpress-plugins/captcha/get-key-and-salt.py).

Voici le tableau des clés et du sel en fonction de la version :

Version	| Clé	| Sel
------------ | ------------- | -------------
2.12 à 2.34	| 123	| BGuxLWQtKweKEMV4
2.4 à 2.4.4	| bws2012	| 5tOYgjaWC2VtdEWQ
3.0 à 3.3	| bws2012	| 5tOYgjaWC2VtdEWQ
3.4 à 3.7	| bws18042013	| 5tOYgjaWC2VtdEWQ
3.7.1 et 3.7.2	| bws18042013	| 5tOYgjaWC2VtdEWQ
3.7.3 à 3.7.7	| bws-17072013	| 5tOYgjaWC2VtdEWQ
3.7.8 et 3.7.9	| bws-23082013	| 5tOYgjaWC2VtdEWQ
3.8.1	| bws-23082013	| 5tOYgjaWC2VtdEWQ

Grâce à cela, j’ai modifié mon précédent script. Il est désormais possible d’obtenir la version du plugin d’un site distant (une analyse du fichier readme est effectuée), de casser un captcha en fonction de la version, ou bien de bruteforcer le captcha. Vous trouverez le script [ici](https://github.com/cervoise/pentest-scripts/blob/master/web/cms/captcha-bypass/wordpress-plugins/captcha/bypass-3.8.1-and-previous.php).













