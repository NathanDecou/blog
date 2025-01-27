---
title: Synoptic code
---

## Objectif

Un code morse a été intercepté le 13 Octobre 2024 depuis le `Yelna` un bateau de la marine russe en mer noire. Il faut retrouver depuis ce code la température mesurer par le navire. Le code est le suivant :

```morse
.-. -.-. ...- / -.. . / ..- -.-. - .- .....
.---- ...-- .---- ---.. .---- / ----. ----. ...-- ....- .....
.---- ----- ...-- ....- -.... / ....- .---- -.... ----. ---..
...-- ..--- ....- ----- ..... / .---- ----- ..--- ---.. -----
....- ----- .---- ..--- ----- / ..... ....- ----- ----- -----
--... ----- ..--- ----- ----- / ---.. ...-- ..... ----- ----- 
..--- ..--- ..--- ..... ..--- / ----- ----- ..--- ---.. ----- 
.---- ...-- ----- .---- ..--- / -... - / .- .-.
..- -.-. - .- ..... / -.
```

## Traduction du morse vers l'alphabet

Le code morse une fois remis en alphabet donne ceci :

```
RCV DE UCTA5 13181 99345 10346 41698 32405 10280 40120 54000 70200 83500 22252 00280 13012 BT AR UCTA5 N
```

En cherchant on tombe sur plusieurs articles et tweet de personne traduisant de tels codes vers des informations tangibles (par exemple ce [tweet de @te3ej](https://x.com/te3ej/status/1845531951370731905)). Cependant, je n'ai pas trouvé comment ils s'y prenaient.

En cherchant 'synoptic code' (le nom du challenge), on trouve qu'il s'agit d'un codage de données servant à transmettre des données météorologiques.

## L'IA à la rescousse

J'ai décidé d'utiliser l'outil [perplexity](https://www.perplexity.ai) et de voir si l'agent était capable de traduire le message. Le message a pu être traduit par l'IA sans soucis. Attention toute fois, on peut voir dans les sources utilisées par perplexity qu'un writeup sur ce challenge est utilisée. Même si les autres sources pourraient probablement suffir à l'outil pour la traduction, il est évident que celle est la plus utile mais constitue presque de la triche.

{{ image(url="perplexity.jpg", no_hover=true) }}

## Solution

La température à trouver est 28.0°C.