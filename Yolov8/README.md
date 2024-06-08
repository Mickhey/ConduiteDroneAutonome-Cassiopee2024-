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

`person_detector_yolov8.py` permet de réaliser l'inférence à partir d'une image. La ligne model.predict permet de choisir différents paramètres importants : l'image, la classe (0 pour personne) et le nombre de détections (ici on ne gère qu'une personne). Enfin, la méthode renvoie l'image qui a été redimensionnée, les coordonnées de la boîte de contour et le barycentre.

Toutes les fonctions `test_*.py` se connectent au drone, activent le flux vidéo et le récupèrent puis font décoller le drone. On lance des timers pour calculer le temps d'inférence et le temps de cycle total. Ensuite, pour chaque image, on lance une inférence et en fonction du résultat on envoie des commandes de contrôle. Chaque test fait cela de manière différente, en utilisant des threads, un PID, etc.

`optimized.py` utilise des threads, un PID, des optimisations (taille de l'image, utilisation GPU) et utilise la librairie djitellopy_optimized pour réduire les temps entre requêtes et minimiser les appels différents.
