# Un peu de triche dans les jeux Facebook

Publication (seconde) : 29 décembre 2013
Publication (première) : été 2010

Cet article est paru sur mon ancien blog. Le sujet étant intéressant, je le re-publie avec quelques corrections.

Il y a quelques années, j’ai voulu battre « mes amis » dans des jeux Facebook. Notamment [Le défi du clic](http://www.facebook.com/#!/apps/application.php?id=131516040209649&ref=ts), jeu consistant à cliquer un maximum de fois en dix secondes et [ABC Challenge](http://www.facebook.com/apps/application.php?id=354325192762&ref=ts), jeu où il faut taper l’alphabet le plus vite possible. Pour cela, j’ai décidé d’utiliser la classe [Java Robot](http://download.oracle.com/docs/cd/E17476_01/javase/1.4.2/docs/api/java/awt/Robot.html). Cependant, avant de partir bille en tête, j’ai effectué un petit tour sur le net afin d’essayer de découvrir des applications pouvant m’aider dans ma tâche, c’est ainsi que j’ai découvert un petit logiciel Windows : [AutoIT](http://www.autoitscript.com/). Il s’agit d’un interpréteur de scripts avec une syntaxe assez simple permettant d’automatiser des tâches Windows. Il permet notamment le déplacement de la souris, le clique, l’ouverture d’applications. Il peut aussi récupérer la couleur d’un pixel spécifique, etc. Cet outil permet de préparer votre station de travail pendant que vous allez prendre un café, en ouvrant les applications et dossiers voulus. Il est aussi utilisé pour tricher, par exemple dans WOW, afin de réaliser des script de farm. Enfin, il sert aussi au [développement de malware](http://code.google.com/p/malware-lu/wiki/en_analyse_autoit_ransomware).

## Premier jeu : Le Défi du Clic

Comme introduit plus haut, le principe du jeu est très simple, un simple bouton ou il faut cliquer le plus grand nombre de fois en 10 secondes. Un première possibilité pour améliorer son score est d’utiliser deux souris, permettant ainsi de doubler la cadence de clic.

### Utilisation d’Auto-IT

Le script est très simple,on commence par attendre 10s comme afin de quitter l’interpréteur Auto-IT et de donner la main à ma page web. Ensuite on lance une boucle de 50 itérations qui va émettre 150 clic gauche au pixel 640, 512. L’inconvénient de cet outil est qu’il faut indiquer la position de la souris. Il est donc nécessaire de bien placer le bouton à cliquer.

#### Script

```
Sleep(1000*10)
For $i = 1 To 50
MouseClick("left" , 640, 512 , 150)
Sleep(1)
Next
 
Exit
```

#### Screen

![Résultat avec Auto-IT](http://www.antoine-cervoise.fr/wp-content/uploads/2012/10/Autoit_clic.png)

On obtient un résultat d’une dizaine de clic par seconde, ce qui est plutôt faible pour un tache automatisée. Pour améliorer les performances du script, il est possible dans lancer plusieurs en parallèles en optimisant bien le timer de départ.

### Utilisation de Java Robot

On utilise a peu près la même structure de code qu’avec AutoIT (notamment pour le Timer).  Le gros avantage ici par rapport à AutoIt est que l’on a pas besoin des coordonnées de la souris, il suffit de bien la placer. Java Robot se contente de cliquer et de relâcher le clic gauche.

```java
Robot robot = new Robot();
int a;
 
robot.delay(10000);
 
for(a = 0 ; a < 200000 ; a++){
robot.mousePress(InputEvent.BUTTON1_MASK);
robot.mouseRelease(InputEvent.BUTTON1_MASK);
}
```

J‘ai réussi à atteindre plus de 19000 clic. Soit une moyenne de 1900 clics par seconde !

## Second jeu : ABC Challenge

### Utilisation d'Auto-IT

Comme précédemment, j’attend 10 secondes puis j’envoie l’alphabet à l’application. J’ai fait l’expérience en envoyant caractère par caractère et cela donne un score légèrement plus faible. On obtient un peu plus de 3s pour taper l’alphabet, le principalement ralentissement semble venir des animations.

```
Sleep(1000*10)
Send("abcdefghijklmnopqrstuvwxyz")
```

### Utilisation de Java Robot

Pour utiliser la bibliothèque il est nécessaire de faire quelques imports :

```java
import java.awt.AWTException;
import java.awt.Robot;
import java.awt.event.InputEvent;
import java.awt.event.KeyEvent;
Script
Robot robot = new Robot();
int a = 30;
 
robot.delay(10000);
robot.keyPress(KeyEvent.VK_A);
robot.delay(a);
robot.keyPress(KeyEvent.VK_B);
robot.delay(a);
robot.keyPress(KeyEvent.VK_C);
robot.delay(a);
robot.keyPress(KeyEvent.VK_D);
robot.delay(a);
robot.keyPress(KeyEvent.VK_E);
robot.delay(a);
robot.keyPress(KeyEvent.VK_F);
robot.delay(a+25);
robot.keyPress(KeyEvent.VK_G);
robot.delay(a);
robot.keyPress(KeyEvent.VK_H);
robot.delay(a);
robot.keyPress(KeyEvent.VK_I);
robot.delay(a);
robot.keyPress(KeyEvent.VK_J);
robot.delay(a);
robot.keyPress(KeyEvent.VK_K);
robot.delay(a);
robot.keyPress(KeyEvent.VK_L);
robot.delay(a);
robot.keyPress(KeyEvent.VK_M);
robot.delay(a);
robot.keyPress(KeyEvent.VK_N);
robot.delay(a);
robot.keyPress(KeyEvent.VK_O);
robot.delay(a);
robot.keyPress(KeyEvent.VK_P);
robot.delay(a);
robot.keyPress(KeyEvent.VK_Q);
robot.delay(a);
robot.keyPress(KeyEvent.VK_R);
robot.delay(a);
robot.keyPress(KeyEvent.VK_S);
robot.delay(a);
robot.keyPress(KeyEvent.VK_T);
robot.delay(a);
robot.keyPress(KeyEvent.VK_U);
robot.delay(a);
robot.keyPress(KeyEvent.VK_V);
robot.delay(a);
robot.keyPress(KeyEvent.VK_W);
robot.delay(a);
robot.keyPress(KeyEvent.VK_X);
robot.delay(a);
robot.keyPress(KeyEvent.VK_Y);
robot.delay(a);
robot.keyPress(KeyEvent.VK_Z);
```

#### Screen

La première chose que l’on remarque c’est que le délai est différent entre F et G; ABC Challenge bloqué à F. J’ai donc rallongé un peu le délai et cela a fonctionné. Le score obtenu ci-dessous a été réalisé avec la variable « a » initialisée à 75.

![Premier test](http://www.cervezhack.fr/wp-content/uploads/2013/01/jRobot_75-300x180.png)

En utilisant le code présent plus haut on obtient un temps de 0.748 s. Le jeu nous retourne « Score incorrect » mais publie quand même le résultat sur notre profil !

![Second test - résultat](http://www.cervezhack.fr/wp-content/uploads/2013/01/jRobot_incorrect-300x179.png)

![Second test - partage](http://www.cervezhack.fr/wp-content/uploads/2013/01/jRobot_0748-300x83.png)



## Petite mise à jour de 2013

Les jeux Facebook cités plus haut n’existant plus, j’ai retenté l’expérience en utilisant un jeu similaire sur [funny-games.biz](http://www.funny-games.biz/fingerfenzy.html). Voici le code et les copies d’écrans. Pour rappel, le delay au début du code, permet de laisser le temps de basculer vers l’application flash afin que le script se lance au bon moment.

#### Script
```java
Robot robot = new Robot();
int a = 0;
 
robot.delay(10000);
robot.keyPress(KeyEvent.VK_A);
robot.keyPress(KeyEvent.VK_B);
robot.keyPress(KeyEvent.VK_C);
robot.keyPress(KeyEvent.VK_D);
robot.keyPress(KeyEvent.VK_E);
robot.keyPress(KeyEvent.VK_F);
robot.keyPress(KeyEvent.VK_G);
robot.keyPress(KeyEvent.VK_H);
robot.keyPress(KeyEvent.VK_I);
robot.keyPress(KeyEvent.VK_J);
robot.keyPress(KeyEvent.VK_K);
robot.keyPress(KeyEvent.VK_L);
robot.keyPress(KeyEvent.VK_M);
robot.keyPress(KeyEvent.VK_N);
robot.keyPress(KeyEvent.VK_O);
robot.keyPress(KeyEvent.VK_P);
robot.keyPress(KeyEvent.VK_Q);
robot.keyPress(KeyEvent.VK_R);
robot.keyPress(KeyEvent.VK_S);
robot.keyPress(KeyEvent.VK_T);
robot.keyPress(KeyEvent.VK_U);
robot.keyPress(KeyEvent.VK_V);
robot.keyPress(KeyEvent.VK_W);
robot.keyPress(KeyEvent.VK_X);
robot.keyPress(KeyEvent.VK_Y);
robot.keyPress(KeyEvent.VK_Z);
```

#### Screen

![Résultat](http://www.cervezhack.fr/wp-content/uploads/2013/01/abc-300x216.jpg)


## Conclusion

En conclusion Java Robot est bien plus efficace et à l’avantage d’être multi-plateformes AutoIT semble permettre beaucoup plus de chose dans l’automatisation de tâches, notamment dans les jeux. Il est très populaire dans WOW (voir MISC n°50 – Juillet/Août 2010 – Dans l’enfer de World of Warcraft). A essayer lorsque l’on veut tricher ! Les différents tests effectués ont aussi montré que le débit de connexion (bas débit/haut débit, wiki/filaire) influence le résultat.



