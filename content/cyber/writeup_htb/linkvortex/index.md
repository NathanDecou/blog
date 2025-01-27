---
title: Machine - linkvortex
---

## Machine
+ URL : [Linkvortex](https://app.hackthebox.com/machines/linkvortex)
+ Difficulté : easy

## Enumération
On enumère les ports TCP ouverts avec `nmap -sV <IP>`.

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-21 09:39 CET
Nmap scan report for linkvortex.htb (10.10.11.47)
Host is up (0.016s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.00 seconds
```

Il ya deux ports ouverts, le 80 avec un serveur web et le 22 en écoute pour une connexion SSH.

## Port 80
### Page d'accueil

En accedant à `<IP>:80` on est redirigé vers `http://linkvortex.htb`. Un blog est hebergé sur cette URL. En explorant rapidement on ne voit rien qui semble interessant.

{{ image(url="homepage.png", no_hover=true) }}

### robots.txt

En allant sur `http://linkvortex.htb/robots.txt`, on recupère le fichier robots.txt du site.

```
User-agent: *
Sitemap: http://linkvortex.htb/sitemap.xml
Disallow: /ghost/
Disallow: /p/
Disallow: /email/
Disallow: /r/
```

On y voit des URLs qui peuvent s'averer interessantes. Notamment l'URL `/ghost`, qui renvoie vers la page de login pour administrer le CMS ([ghost](https://ghost.org))

{{ image(url="login_page.png", no_hover=true) }}

## Retour à de l'énumération

Après avoir tenté plusieurs couple login/password sans succès, on retourne enumérer pour voir si on a rien oublié.

### Fuzz de vhost

On tente de voir si quelque chose d'autre est hebergé par ce serveur web. Pour ça on va tenter de remplacer le champ `Host` dans la requete http et voir ce qui répond. On automatise cette tache avec `gobuster`.

```
└─ $ gobuster vhost -w vhost_fuzz.txt --url 10.10.11.47 --domain linkvortex.htb --append-domain
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://10.10.11.47
[+] Method:          GET
[+] Threads:         10
[+] Wordlist:        vhost_fuzz.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Found: dev.linkvortex.htb Status: 200 [Size: 2538]
Progress: 153 / 154 (99.35%)
===============================================================
Finished
===============================================================
```

On voit qu'on a une réponse pour `dev.linkvortex.htb`.

## dev.linkvortex.htb

Cette page ne semble rien donner. Juste une image nous disant que le site arrive bientôt.

{{ image(url="dev_linkvortex.png", no_hover=true) }}

On lance dans le doute une recherche de repertoire avec `dirsearch`. On trouve alors un dossier `.git` accessible.

{{ image(url="found_git.png", no_hover=true) }}

### Exploration du depot git

On télécharge le dossier (`wget --no-parent -r http://dev.linkvortex.htb/.git`) et on restaure le depot (`git checkout .`). Voici l'architecture du dépot.

```
└─ $ tree -L 1
.
├── apps
├── ghost
├── LICENSE
├── nx.json
├── package.json
├── PRIVACY.md
├── README.md
├── SECURITY.md
└── yarn.lock
```


C'est un fork du depot git de ghost. En faisant `git status` on voit que 2 fichiers ont été modifiés. Un a été ajouté et l'autre modifié.

```
└─ $ git status
Actuellement sur aucune branche.
Modifications qui seront validées :
  (utilisez "git restore --staged <fichier>..." pour désindexer)
        nouveau fichier : Dockerfile.ghost
        modifié :         ghost/core/test/regression/api/admin/authentication.test.js
```

Si on regarde de plus près ce qui a été modifié, on voit que dans le fichier `authentication.test.js`, la chaine `thisissupersafe` est devenue `OctopiFociPilfer45`.

```
└─ $ git diff --cached ghost/
diff --git a/ghost/core/test/regression/api/admin/authentication.test.js b/ghost/core/test/regression/api/admin/authentication.test.js
index 2735588..e654b0e 100644
--- a/ghost/core/test/regression/api/admin/authentication.test.js
+++ b/ghost/core/test/regression/api/admin/authentication.test.js
@@ -53,7 +53,7 @@ describe('Authentication API', function () {

         it('complete setup', async function () {
             const email = 'test@example.com';
-            const password = 'thisissupersafe';
+            const password = 'OctopiFociPilfer45';  <--- mot de passe changé
```

Si on essaie d'utiliser ce mot de passe en combinaison avec le mail `admin@linkvortex.htb`, on arrive à se connecter à l'interface.

{{ image(url="admin_page.png", no_hover=true) }}

## Accès au serveur

En regardant le code source des pages sur le blog on peut y voir `<meta name="generator" content="Ghost 5.58">`. Nous indiquant donc que la version utilisée de ghost est la `5.58`.

Cette version est vulnérable à la [CVE 2023-40028](https://nvd.nist.gov/vuln/detail/CVE-2023-40028). Cette vulnérabilité permet à un utilisateur authentifié de lire des fichiers sur le système (en uploadant des images qui sont en fait des liens symboliques vers ces fichiers).

Plusieurs POC existent pour exploiter cette vulnérabilité, j'ai utilisé celui ci : [POC CVE 2023-40028 - 0xyassine](https://github.com/0xyassine/CVE-2023-40028)

Dans le dépot git que l'on a récupéré se trouve le fichier `Dockerfile.ghost`. Une des directives présentes est `COPY config.production.json /var/lib/ghost/config.production.json`.

Ce fichier (`/var/lib/ghost/config.production.json`) semble être une bonne cible pour notre exploitation de la CVE.

En voici le contenu (tronqué pour faciliter la lecture):

```json
{
  "url": "http://localhost:2368",
  "server": {
    "port": 2368,
    "host": "::"
  },
  <TRUNCATED>
  "mail": {
     "transport": "SMTP",
     "options": {
      "service": "Google",
      "host": "linkvortex.htb",
      "port": 587,
      "auth": {
        "user": "bob@linkvortex.htb",   <----- login
        "pass": "fibber-talented-worth" <----- password
        }
      }
    }
}
```

On peut y voir un couple username/password (`bob@linkvortex.htb`/`fibber-talented-worth`).

En essayant ce couple en SSH, on accède à la machine.

{{ image(url="logged_user.png", no_hover=true) }}

## Recuperation du flag root

En lançant `sudo -l`, on voit que l'utilisateur `bob` peut lancer en sudo la commande `/usr/bin/bash /opt/ghost/clean_symlink.sh *.png`

Voici le contenu du script.

```sh
#!/bin/bash

QUAR_DIR="/var/quarantined"

if [ -z $CHECK_CONTENT ];then
  CHECK_CONTENT=false
fi

LINK=$1

if ! [[ "$LINK" =~ \.png$ ]]; then
  /usr/bin/echo "! First argument must be a png file !"
  exit 2
fi

if /usr/bin/sudo /usr/bin/test -L $LINK;then
  LINK_NAME=$(/usr/bin/basename $LINK)
  LINK_TARGET=$(/usr/bin/readlink $LINK)
  if /usr/bin/echo "$LINK_TARGET" | /usr/bin/grep -Eq '(etc|root)';then
    /usr/bin/echo "! Trying to read critical files, removing link [ $LINK ] !"
    /usr/bin/unlink $LINK
  else
    /usr/bin/echo "Link found [ $LINK ] , moving it to quarantine"
    /usr/bin/mv $LINK $QUAR_DIR/
    if $CHECK_CONTENT;then
      /usr/bin/echo "Content:"
      /usr/bin/cat $QUAR_DIR/$LINK_NAME 2>/dev/null
    fi
  fi
fi
```

Ce script sert à deplacer des fichiers `png` qui sont en fait des liens symboliques vers un dossier de quarantaine. Voici les 2 caractéristiques importantes du script :

+ Une variable d'environnement permet ou non de lire le contenu du fichier pointé.
+ Si le fichier pointé contient 'root' ou 'etc', le lien sera supprimé et aucune lecture du fichier ne sera possible

Notre but est de lire le fichier `/root/root.txt` (fichier contenant le flag sur les machines HTB), il nous faut donc bypasser ce deuxième point.

Pour cela, il suffit de faire deux liens. Le premier qui pointera vers `/root/root.txt`, le second vers le premier. Et on utilisera le premier avec le script.

{{ image(url="proc_root.png", no_hover=true) }}

Nous avons donc réussi à lire le fichier `/root/root.txt`.