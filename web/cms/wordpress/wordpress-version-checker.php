<?php
/*
|s C R i P T z - T E A M . i N F O|
A. Cervoise - 10/20/2012
WordPress Version Checker - MD5 Hash Method
*/
 
define("SiTE", "http://net.tutsplus.com/"); //SiTE TO BE CHECKED
define("CHECK_FiLE", "/wp-includes/js/tinymce/tiny_mce.js"); //FiLE TO BE CHECKED
 
/*
WP VERSiON   :  MD5 HASH
2.0 - 2.0.1 - 2.0.4 - 2.0.5 - 2.0.6 - 2.0.7 - 2.0.8 - 2.0.9 - 2.0.10 - 2.0.11 :
a306a72ce0f250e5f67132dc6bcb2ccb
2.1 - 2.1.1 - 2.1.2 - 2.1.3
4f04728cb4631a553c4266c14b9846aa
2.2 - 2.2.1 - 2.2.2 - 2.2.3 :
25e1e78d5b0c221e98e14c6e8c62084f
2.3 - 2.3.1 - 2.3.2 - 2.3.3 :
83c83d0f0a71bd57c320d93e59991c53
2.5 :
7293453cf0ff5a9a4cfe8cebd5b5a71a
2.5.1 :
a3d05665b236944c590493e20860bcdb
2.6 - 2.6.1 - 2.6.2 - 2.6.3 - 2.6.5 :
61740709537bd19fb6e03b7e11eb8812
2.7 - 2.7.1 :
e6bbc53a727f3af003af272fd229b0b2
2.8 - 2.8.1 - 2.8.2 - 2.8.3 - 2.8.4 - 2.8.5 - 2.8.6 :
56c606da29ea9b8f8d823eeab8038ee8
2.9 - 2.9.1 - 2.9.2 - 3.0 - 3.0.1 - 3.0.2 - 3.0.3 - 3.0.4 - 3.0.5 - 3.0.6 :
128e75ed19d49a94a771586bf83265ec
3.1 :
82ac611e3da57fa3e9973c37491486ee
3.1.1 - 3.1.2 - 3.1.3 - 3.1.4 :
e52dfe5056683d653536324fee39ca08
3.2 - 3.2.1 :
a57c0d7464527bc07b34d675d4bf0159
3.3 - 3.3.1 - 3.3.2 - 3.3.3 :
9754385dabfc67c8b6d49ad4acba25c3
3.4 - 3.4.1 - 3.4.2 :
7424043e0838819af942d2fc530e8469
*/
 
echo md5(file_get_contents(SiTE.CHECK_FiLE)); //DO iT!
?>
