---
title: Hot stuff
---

## Objectif
L'objectif est de trouver le numéro d'immatriculation ainsi que le numéro peint sur l'hélicoptère apparaissant sur la photo suivante. Au format AB-CDE-99.

{{ image(url="https://challenge.bellingcat.com/assets/fire_fight-VpUZRvdF.jpg", alt="Photo de l'helicoptère à trouver", no_hover=true) }}

## Le numéro d'immatriculation
Je vais commencer par chercher le numéro d'immatriculation (aussi appelé 'tail number'). Il se trouve sur la queue de l'appareil.


### Simple zoom

Sur la photo fournie, le numéro est illisible même en zoomant sur l'appareil.
{{ image(url="zoom.jpg", alt="Zoom sur l'helicoptère à trouver", no_hover=true) }}

### Reverse search
Une bonne façon pour retrouver une image est d'utilisée la recherche inversée avec [Google images](https://images.google.com/) par exemple.

En faisant cette recherche avec notre image, on tombe rapidement sur cette image

{{ image(url="https://cdn.plnspttrs.net/31042/ec-mqr-bombers-generalitat-de-catalunya-eurocopter-as-350b-3-ecureuil_PlanespottersNet_1611269_188fe12e18_o.jpg", alt="Image similaire", no_hover=true) }}

Il s'agit du même hélicoptère, avec le numéro 21 peint sur dessus. La photo est bien plus net et le numéro d'immatriculation y est visible : `EC-MQR`.

## Le numéro peint
L'énoncé du challenge nous indique qu'il a changé depuis la photo que l'on possède, il nous faut donc trouver le bon numéro.

En cherchant 'EC-MQR' sur Google on trouve une série de photos sur le site www.jetphotos.com. Voici le lien vers la série de photos https://www.jetphotos.com/registration/EC-MQR.

La photo la plus récente est celle ci

{{ image(url = "https://cdn.jetphotos.com/full/6/800916_1721103664.jpg", alt="Photo du 11 Juillet 2024 de l'helicoptère",no_hover=true) }}

Le numéro est donc le 11

## Solution
La solution est donc `EC-MQR-11.`