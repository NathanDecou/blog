---
title: Up the creek
---

Premier exercice des [challenges Bellingcat](https://challenge.bellingcat.com)

## Objectif
Trouver le nom de la rivière sur la photo suivante :

{{ image(url="https://challenge.bellingcat.com/assets/river_view-CKtDD37P.jpg", alt="Page d'accueil du site", no_hover=true) }}

## Recherche
### Données EXIF
On commence par verifier les metadatas de l'image en examinant les données exifs.

Via l'outil `exiftool` on récupère les données GPS suivantes :

```shell
GPS Latitude                    : 47 deg 41' 39.33" N
GPS Longitude                   : 121 deg 59' 41.77" W
```



### Nom de la rivière
En se rendant à ces coordonnées (47°41'39.33"N 121°59'41.77"W) sur [google maps](https://www.google.com/maps/place/47%C2%B041'39.3%22N+121%C2%B059'41.8%22W/) nous pouvons confirmer qu'il s'agit du bon emplacement 

{{ image(url="maps.jpg", alt="Vue satellite de l'emplacement", no_hover=true) }}

## Solution

La rivière est donc la 'Snoqualmie'.