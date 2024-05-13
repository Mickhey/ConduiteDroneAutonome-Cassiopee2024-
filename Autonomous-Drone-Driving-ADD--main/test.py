from djitellopy import Tello
import cv2, math, time
import run_person_detector as detector
import numpy as np
import matplotlib.pyplot as plt

# Initialisation du drone
tello = Tello()
tello.connect()
print(tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()
tello.move_up(60)  # s'élève de 60cm en plus pour être à hauteur humaine

# Initialisation des listes pour stocker les temps
cycle_times = []
inference_times = []

for i in range(50):
    start = time.time()
    image = frame_read.frame
    temps_calcul_start = time.time()
    result, coordinates, barycenter = detector.run_object_detection(image)  # Exécute la détection de personne sur l'image
    temps_calcul_end = time.time()

    # Enregistrer les temps
    inference_time = temps_calcul_end - temps_calcul_start
    inference_times.append(inference_time)

    if coordinates != [0, 0, 0, 0]:  # si on détecte quelqu'un
        bx = barycenter[0]  # Coordonnée x du barycentre
        by = barycenter[1]  # Coordonnée y du barycentre

        if bx > 448:
            tello.rotate_clockwise(10)
        elif bx < 408:
            tello.rotate_counter_clockwise(10)

    end = time.time()
    cycle_time = end - start
    cycle_times.append(cycle_time)

    print(f"{i + 1}ème image")
    print("Délai par cycle en secondes:", cycle_time)
    print("Temps d'inférence + calcul barycentre:", inference_time)

# Calculer les moyennes des temps enregistrés
average_cycle_time = sum(cycle_times) / len(cycle_times)
average_inference_time = sum(inference_times) / len(inference_times)

print("Temps moyen par cycle:", average_cycle_time)
print("Temps moyen d'inférence:", average_inference_time)

tello.land()
tello.streamoff()
tello.end()
