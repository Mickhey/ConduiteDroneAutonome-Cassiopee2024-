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

## Installation

### Prérequis

- Python 3.6 ou supérieur
- pip (gestionnaire de paquets pour Python)

### Étapes

1. Clone du dépot :

- git clone <https://github.com/Mickhey/ConduiteDroneAutonome-Cassiopee2024-.git>
- cd Autonomous-Drone-Driving-ADD--main

1. Installation des dépendances

- Installation de djitellopy via pip install djitellopy
- Installation de ultralytics : [Ultralytics quickstart](https://docs.ultralytics.com/quickstart/) (Choisir en fonction de son PC)

## Utilisation

1. Mettre le drone en route et le connecter a la wifi de son ordinateur.
2. Executer un des test_Yolov8_*.py

## Optimisations et Améliorations

- **Passage de YOLOv4 à YOLOv8** : Amélioration de la précision et réduction des temps d'inférence.
- **Utilisation d'un PID** : Utilisation d'un PID pour la rotation pour avoir un contrôle plus fluide.
- **Utilisation de Threads** : Optimisation des temps d'inférence et des performances globales du système.
- **Tests de Performance** : Inclusion de tests pour mesurer les performances du système en termes de latence et de précision.
