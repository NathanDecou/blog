---
title: Machine - underpass
---

## Machine
+ URL : [Underpass](https://app.hackthebox.com/machines/UnderPass)
+ Difficulté : easy


## Enumération initiale
Enumeration TCP via `nmap -sV <IP>`

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-17 13:06 CET
Nmap scan report for underpass.htb (10.10.11.48)
Host is up (0.012s latency).
Not shown: 998 closed tcp ports (conn-refused)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.52 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Enumeration UDP via `nmap -sU <IP>`

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-17 11:07 CET
Nmap scan report for underpass.htb (10.10.11.48)
Host is up (0.015s latency).
Not shown: 97 closed udp ports (port-unreach)
PORT     STATE         SERVICE
161/udp  open          snmp
1812/udp open|filtered radius
1813/udp open|filtered radacct

Nmap done: 1 IP address (1 host up) scanned in 115.88 seconds
```

## Port 80
En se rendant sur le port 80 de la machine via un navigateur web on tombe sur la page par défaut d'Apache2 pour Ubuntu.

## Port 161
Le port 161 est en ecoute pour le service SNMP. On peut en tirer des informations via `snmp-check <IP>`

```
snmp-check v1.9 - SNMP enumerator
Copyright (c) 2005-2015 by Matteo Cantoni (www.nothink.org)

[+] Try to connect to 10.10.11.48:161 using SNMPv1 and community 'public'

[*] System information:

  Host IP address               : 10.10.11.48
  Hostname                      : UnDerPass.htb is the only daloradius server in the basin!
  Description                   : Linux underpass 5.15.0-126-generic #136-Ubuntu SMP Wed Nov 6 10:38:22 UTC 2024 x86_64
  Contact                       : steve@underpass.htb
  Location                      : Nevada, U.S.A. but not Vegas
  Uptime snmp                   : 04:54:08.70
  Uptime system                 : 04:53:58.28
  System date                   : 2025-1-20 08:55:30.0
```

La partie `hostname` nous donne l'information que ce serveur heberge [daloradius](https://www.daloradius.com/), un GUI web pour manager un serveur FreeRadius.

## Enumeration de repertoire sur le serveur web
On va essayer d'énumérer des potentiels repertoires qui pourraient être sur `http://<IP>/daloradius`.

On utilise `dirsearch -u http://<IP>/daloradius -r`.

On trouve notamment ces deux URLs qui sont deux pages de login :

+ http://<IP>/daloradius/app/users/login.php
+ http://<IP>/daloradius/app/operators/login.php

## Accès au dashboard daloradius

Sur la doc de daloradius, on trouve que le couple `login:password` par defaut est `administrator:radius`

En testant sur les deux URLs precedemment trouvée, ce couple fonctionne pour `/operators/login.php`

{{ image(url="dashboard_daloradius.jpg", no_hover=true) }}

## Accès au serveur

Via le dashboard il est possible de lister les utilisateurs. Ceci nous donne aussi le hash de leur mot de passe.

{{ image(url="list_users.jpg", no_hover=true) }}

On peut alors essayer de trouver le mot de passe en clair de l'utilisateur. Via [crackstation](https://crackstation.net/) par exemple.

{{ image(url="hash_crack.jpg", no_hover=true) }}

Le mot de passe de l'utilisateur `svcMosh` est `underwaterfriends`.

Les machines Hackthebox utilisent souvent le même procédé : un mot de passe trouvé sera souvent le mot de passe du même utilisateur sur la machine.

En testant de se connecter en SSH en tant que `svcMosh` sur la machine avec le mot de passe `underwaterfriends`, on n'echappe pas à la règle et la connnexion fonctionne. On récupère donc le flag `user`.

{{ image(url="logged.jpg", no_hover=true) }}

## Flag root
### Listing sudo

En tant que `svcMosh` on lance `sudo -l` pour voir à quoi l'on a accès. On voit que l'on peut lancer `/usr/bin/mosh-server` sans mot de passe en tant que root.

```
svcMosh@underpass:~$ sudo -l
Matching Defaults entries for svcMosh on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User svcMosh may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/bin/mosh-server
```

### Analyse du fichier `/usr/bin/mosh-server`

Il s'agit d'un binaire lié à `mosh`, un outil permettant de remplacer les shell interactifs SSH.

En regardant la documentation on voit que `mosh-server` permet de lancer un serveur mosh auquel un client mosh pourra se connecter. En lançant `sudo mosh-server`, on lance donc un serveur mosh en tant que root.

Une fois ce serveur lancer, il nous suffit de faire `MOSH_KEY='<KEY>' mosh-client <IP> <PORT>` pour se connecter au serveur et etre root ! Les valeurs de `<PORT>` et de `<KEY>` sont données par le retour de la commande `sudo mosh-server`.


{{ image(url="root_logged.jpg", no_hover=true) }}

And voila, nous sommes `root` sur cette machine.