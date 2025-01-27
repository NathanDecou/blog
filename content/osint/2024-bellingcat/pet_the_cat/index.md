---
title: "Pet the cat"
---

## Objectif
Trouver la ville où a été prise la photo suivante 

{{ image(url="https://challenge.bellingcat.com/assets/cat-DfQ7rjFA.jpg", alt="Photo à géolocaliser", no_hover=true) }}

## Recherche de la ville
### EXIF
Malheuresement, rien dans les metadatas de l'image ne nous donne d'informations quant à l'endroit où a pu être prise la photo.

### Recherche inversée
J'utilise donc la recherche d'image inversée de [Google Images](https://images.google.com). En jouant un peu avec le cadre permettant de définir la zone à analyser, on tombe sur des images comme celles ci.

{{ image(url="https://st4.depositphotos.com/1023102/20539/i/1600/depositphotos_205394182-stock-photo-view-old-town-kotor-kotor.jpg", no_hover=true) }}

{{ image(url="https://viagallica.com/montenegro/img/ville_kotor_-_ville_close_020_(palais_drago).jpg", no_hover=true) }}

Le batiment sur ces deux images ressemble beaucoup à celui au fond de la photo à localiser. Le batiment est à Kotor, au Montenegro.

## Recherche de l'endroit précis

Pour s'assurer, qu'il s'agit bien de Kotor je cherche l'endroit précis où a été prise la photo. Il n'y a presque aucun street view à Kotor. Cependant, c'est une ville touristique, il y a donc souvent des vidéos de personne se filmant en train de parcourir la ville à pied.

En cherchant 'Kotor walk' sur YouTube on trouve par exemple cette vidéo

{{ youtube(id="PCm8Sdpmh-0") }}

A exactement 5mn29 on y voit ce plan

{{ image(url="kotor_screen.jpg", no_hover=true)}}

On peut y reconnaitre le batiment en fond de la photo originale à gauche, et l'architecture de la barrière en pierre à droite.

Voici une comparaison des deux photographies.

{{ image(url="comparaison.jpg", no_hover=true) }}

## Solution
La photo a été prise à Kotor.