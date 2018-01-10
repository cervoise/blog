# WordPress Version Checker, nouvelle liste de MD5

Publication : 20 octobre 2012

La semaine passé, Scriptz Team a publié un script permettant de déterminer à distance la version de WordPress utilisée sur un site. Le script original est disponible [ici](http://pastebin.com/3c72K1kj/).

Ce script analyse le condensat md5 du fichier /wp-includes/js/tinymce/tiny_mce.js afin de déterminer la version de WordPress. Ce fichier étant apparu dans la version 2.0 de WordPress, cette méthode ne permet donc pas de détecter des versions antérieures à la 2.0.

Après vérification, en utilisant les anciennes versions de WordPress, accessibles [ici](http://wordpress.org/download/release-archive/), je n’ai pas la même liste de condensat que celle présente sur pastebin. J’ai alors contacté s C R i P T z – T E A M . i N F O qui m’a répondu:

> It was to show how it can works, you can modify as you want :)

Donc voici la liste de MD5 que j’ai calculé :

WordPress Version	| Condensat MD5 de /wp-includes/js/tinymce/tiny_mce.js
------------ | -------------
2.0; 2.0.1; 2.0.4; 2.0.5; 2.0.6; 2.0.7; 2.0.8; 2.0.9; 2.0.10; 2.0.11 | a306a72ce0f250e5f67132dc6bcb2ccb
2.1; 2.1.1; 2.1.2; 2.1.3 | 4f04728cb4631a553c4266c14b9846aa
2.2; 2.2.1; 2.2.2; 2.2.3 | 25e1e78d5b0c221e98e14c6e8c62084f
2.3; 2.3.1; 2.3.2; 2.3.3 | 83c83d0f0a71bd57c320d93e59991c53
2.5 | 7293453cf0ff5a9a4cfe8cebd5b5a71a
2.5.1 | a3d05665b236944c590493e20860bcdb
2.6; 2.6.1; 2.6.2; 2.6.3; 2.6.5 | 61740709537bd19fb6e03b7e11eb8812
2.7; 2.7.1 | e6bbc53a727f3af003af272fd229b0b2
2.8; 2.8.1; 2.8.2; 2.8.3; 2.8.4; 2.8.5; 2.8.6 | 56c606da29ea9b8f8d823eeab8038ee8
2.9; 2.9.1; 2.9.2; 3.0; 3.0.1; 3.0.2; 3.0.3; 3.0.4; 3.0.5; 3.0.6 | 128e75ed19d49a94a771586bf83265ec
3.1 | 82ac611e3da57fa3e9973c37491486ee
3.1.1; 3.1.2; 3.1.3; 3.1.4 | e52dfe5056683d653536324fee39ca08
3.2; 3.2.1 | a57c0d7464527bc07b34d675d4bf0159
3.3; 3.3.1; 3.3.2; 3.3.3 | 9754385dabfc67c8b6d49ad4acba25c3
3.4; 3.4.1; 3.4.2 | 7424043e0838819af942d2fc530e8469

Il y a quelques version de WordPress qui sont manquantes dans cette liste (2.0.2, 2.0.3 and 2.6.4), elles ne sont pas disponibles sur le site wordpress.org.

Donc voici une nouvelle version du [script](https://github.com/cervoise/blog/blob/master/cms/wordpress/wordpress-version-checker.php).


# WordPress Version Checker, new MD5 list

Publication : 10/20/2012

Last week, Scriptz Team published a script for remotly determinate WordPress version use on a website. You can find the orignial script [here](http://pastebin.com/3c72K1kj/).

This script checks md5 sum of /wp-includes/js/tinymce/tiny_mce.js file for determinate WordPress version. This file was added in WordPress in version 2.0. So it do not works with older versions.

After checking with WordPress old realeases from [here](http://wordpress.org/download/release-archive/), I have’nt the same checksum than on pastebin. I’ve contacted s C R i P T z – T E A M . i N F O and they reply:

> It was to show how it can works, you can modify as you want :)

The MD5 sums I’ve found:

WordPress Version	| Condensat MD5 de /wp-includes/js/tinymce/tiny_mce.js
------------ | -------------
2.0; 2.0.1; 2.0.4; 2.0.5; 2.0.6; 2.0.7; 2.0.8; 2.0.9; 2.0.10; 2.0.11 | a306a72ce0f250e5f67132dc6bcb2ccb
2.1; 2.1.1; 2.1.2; 2.1.3 | 4f04728cb4631a553c4266c14b9846aa
2.2; 2.2.1; 2.2.2; 2.2.3 | 25e1e78d5b0c221e98e14c6e8c62084f
2.3; 2.3.1; 2.3.2; 2.3.3 | 83c83d0f0a71bd57c320d93e59991c53
2.5 | 7293453cf0ff5a9a4cfe8cebd5b5a71a
2.5.1 | a3d05665b236944c590493e20860bcdb
2.6; 2.6.1; 2.6.2; 2.6.3; 2.6.5 | 61740709537bd19fb6e03b7e11eb8812
2.7; 2.7.1 | e6bbc53a727f3af003af272fd229b0b2
2.8; 2.8.1; 2.8.2; 2.8.3; 2.8.4; 2.8.5; 2.8.6 | 56c606da29ea9b8f8d823eeab8038ee8
2.9; 2.9.1; 2.9.2; 3.0; 3.0.1; 3.0.2; 3.0.3; 3.0.4; 3.0.5; 3.0.6 | 128e75ed19d49a94a771586bf83265ec
3.1 | 82ac611e3da57fa3e9973c37491486ee
3.1.1; 3.1.2; 3.1.3; 3.1.4 | e52dfe5056683d653536324fee39ca08
3.2; 3.2.1 | a57c0d7464527bc07b34d675d4bf0159
3.3; 3.3.1; 3.3.2; 3.3.3 | 9754385dabfc67c8b6d49ad4acba25c3
3.4; 3.4.1; 3.4.2 | 7424043e0838819af942d2fc530e8469

There is some version missing in this list (2.0.2, 2.0.3 and 2.6.4), there aren’t available on wordpress.org website.

So you can find a new version of the script [here](https://github.com/cervoise/blog/blob/master/cms/wordpress/wordpress-version-checker.php).
