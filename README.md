# Contrôle et Suivi de Personne avec un Drone TelloEdu

## Description

Ce projet utilise la librairie `djitellopy` pour contrôler un drone TelloEdu et suivre une personne en temps réel. La branche actuelle du projet passe de l'utilisation de YOLOv4 à YOLOv8, apportant des optimisations significatives sur les temps d'inférence grâce à l'utilisation de threads. Des tests de performance et de mesure sont également inclus pour évaluer l'efficacité du système.

## Table des Matières

- [Contrôle et Suivi de Personne avec un Drone TelloEdu](#contrôle-et-suivi-de-personne-avec-un-drone-telloedu)
  - [Description](#description)
  - [Table des Matières](#table-des-matières)
  - [Installation](#installation)
    - [Prérequis](#prérequis)
    - [Étapes](#étapes)
  - [Utilisation](#utilisation)
  - [Optimisations et Améliorations](#optimisations-et-améliorations)
  - [Endroit du code important](#endroit-du-code-important)

## Installation

### Prérequis

- Python 3.6 ou supérieur
- pip (gestionnaire de paquets pour Python)

### Étapes

1. Clone du dépot :

- git clone <https://github.com/Mickhey/ConduiteDroneAutonome-Cassiopee2024-.git>
- cd Autonomous-Drone-Driving-ADD--main

2. Installation des dépendances

- Installation de djitellopy via pip install djitellopy
- Installation de ultralytics : [Ultralytics quickstart](https://docs.ultralytics.com/quickstart/) (Choisir en fonction de son PC)

## Utilisation

1. Mettre le drone en route et le connecter a la wifi de son ordinateur.
2. Executer un des test_Yolov8_*.py
3. Executer optimized.py pour les meilleurs performance.

## Optimisations et Améliorations

- **Passage de YOLOv4 à YOLOv8** : Amélioration de la précision et réduction des temps d'inférence.
- **Utilisation d'un PID** : Utilisation d'un PID pour la rotation pour avoir un contrôle plus fluide.
- **Utilisation de Threads** : Optimisation des temps d'inférence et des performances globales du système.
- **Tests de Performance** : Inclusion de tests pour mesurer les performances du système en termes de latence et de précision.

## Endroit du code important

`person_detector_yolov8.py` permet de réaliser l'inférence à partir d'une image, la ligne model.predict permet de choisir différents paramètres importants, l'image, la classe (0 pour personne) et le nombre de detection (ici on ne gère que une personne). Enfin, la méthode renvoie l'image qui à été redimensionner, les coordonnées de la boite de contour et le barycenre.

Toutes les fonctions `test_*.py`. Elles font toute la même chose, elles se connecte au drone, active le flux vidéo et le récupère puis on fait décoller le drone. On lance des timers pour calculer le temps d'inférence et le temps de cycle total. Ensuite, chaque image on lance un inférence et en fonction du résultat on envoie des commandes de controles. Chaque test fait ça de manière différence, utilisation de thread, pid.

`optimized.py` la méthode utilise des threads, un pid des optimisations (taille de l'image utilisation GPU) et utilise la librairy `djitellopy_optimized` ou on réduit les temps entre requete pour avoir moins de time.sleep et on change les fonctions de rotations pour avoir moins d'appel différent.
