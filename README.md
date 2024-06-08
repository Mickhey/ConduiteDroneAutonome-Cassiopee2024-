# Suivi de Personne en Temps Réel avec un Drone TelloEdu

## Description

Ce projet utilise la librairie `djitellopy` pour contrôler un drone TelloEdu et suivre une personne en temps réel. Le dépôt est structuré en trois versions différentes du système de suivi : une version utilisant YOLOv4, une version utilisant YOLOv8, et une version optimisée avec PID utilisant YOLOv8.

## Table des Matières

- [Suivi de Personne en Temps Réel avec un Drone TelloEdu](#suivi-de-personne-en-temps-réel-avec-un-drone-telloedu)
  - [Description](#description)
  - [Table des Matières](#table-des-matières)
  - [Dossiers du Projet](#dossiers-du-projet)
    - [YOLOv4](#yolov4)
    - [YOLOv8](#yolov8)
    - [YOLOv8\_PID](#yolov8_pid)
  - [Github de l'année d'avant](#github-de-lannée-davant)

## Dossiers du Projet

### YOLOv4

Ce dossier contient la version originale du projet utilisant l'algorithme YOLOv4 pour le suivi de personne. Les scripts dans ce dossier permettent de contrôler le drone TelloEdu et de suivre une personne en utilisant le modèle YOLOv4.

### YOLOv8

Ce dossier contient une version améliorée du projet utilisant YOLOv8, offrant de meilleures performances et une plus grande précision dans la détection de personne. Les scripts de ce dossier utilisent des optimisations pour réduire les temps d'inférence.

### YOLOv8_PID

Ce dossier contient la version la plus avancée du projet, utilisant YOLOv8 avec des réglages PID pour un contrôle plus fluide et précis du drone. En plus des scripts de détection, ce dossier inclut des scripts supplémentaires pour configurer et ajuster les paramètres PID.

## Github de l'année d'avant

- [Github Cassiopée 2023](https://github.com/Witaek/Autonomous-Drone-Driving-ADD-?tab=readme-ov-file)