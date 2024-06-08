from djitellopy import Tello
import cv2
import time
import person_detector_yolov8 as detector
import numpy as np

# Profilage
import cProfile

# Profiler le script entier
profiler = cProfile.Profile()
profiler.enable()

# Initialisation du drone
tello = Tello()
tello.connect()
print("Batterie:", tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

latency = []
calcul_latency = []

tello.takeoff()
tello.move_up(60)  # s'élève de 60cm en plus pour être à hauteur humaine

for i in range(50):  # boucle while serait meilleure mais flemme de traiter comment arrêter la boucle
    start = time.time()
    image = frame_read.frame


    temps_calcul_start = time.time()
    result, coordinates, barycenter = detector.run_object_detection(image)  # Exécute la détection de personne sur l'image
    temps_calcul_end = time.time()
    
    if coordinates != [0, 0, 0, 0]:  # si on détecte quelqu'un
        rapport = (coordinates[1] - coordinates[0]) / (coordinates[3] - coordinates[2])
        bx = barycenter[0]  # Coordonnée x du barycentre
        by = barycenter[1]  # Coordonnée y du barycentre
    end = time.time()
    
    print("i ème image", i)
    print("délai en secondes", end - start)
    print("temps d'inférence + calcul barycentre", temps_calcul_end - temps_calcul_start)
    latency.append(end - start)
    calcul_latency.append(temps_calcul_end - temps_calcul_start)

average_latency = sum(latency) / len(latency)
average_calcul_latency = sum(calcul_latency) / len(calcul_latency)

print("Temps de latence moyen", average_latency)
print("Temps de calcul moyen", average_calcul_latency)

tello.land()
tello.streamoff()
tello.end()

# Fin profilage
profiler.disable()
profiler.dump_stats("output.prof")
