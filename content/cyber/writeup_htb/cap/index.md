---
title: Machine - cap
---

## Machine
+ URL : [Underpass](https://app.hackthebox.com/machines/cap)
+ Difficulté : easy

## Enumaration
On utilise nmap pour lister le nombre de ports ouverts : `nmap <IP>`. Il y a 3 ports ouverts (80,21 et 22)

Sur le port 80, on a un dashboard. Sur le menu de gauche, on a un bouton permettant de générer des "security snapshots". A chaque clic, on est redirigé vers `/data/<ID>`, avec `<ID>` l'identifiant du scan.

En remplaçant `ID` par un autre nombre on accède à d'anciens snapshot. Notamment le premier (id 0).

{{ image(url="snap0.jpg", no_hover=true) }}

## Analyse du pcap

On peut télécharger le `.pcap` associé à ce scan. En l'analysant (avec [https://apackets.com/](https://apackets.com/) par exemple), on voit que des connexions TCP ont été capturées. On t voit apparaître le mot de passe en clair.

{{ image(url="creds_tcp.jpg", no_hover=true) }}


## Accès à la machine

En essayant ce mot de passe pour une connexion SSH, ça fonctionne. Nous avons donc accès à la machine et le flag user.

{{ image(url="logged_user.jpg", no_hover=true) }}

## Accès root

On lance linpeas sur la machine, et on trouve que le binaire `/usr/bin/python3.8` à la capability `CAP_SETUID`. On peut donc exploiter cette capability pour lancer un process en tant que root : `/usr/bin/python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`. Cette commande va ouvrir un shell en tant que root (uid = 0)

{{ image(url="root.jpg", no_hover=true) }}

On recupere ensuite le flag root.