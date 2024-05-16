from djitellopy import Tello
import time
import run_person_detector as detector
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Initialisation du drone
tello = Tello()
tello.connect()
print("Batterie:", tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()
tello.move_up(60)  # s'élève de 60cm en plus pour être à hauteur humaine

# Paramètres PID initiaux
k_p = 0.1
k_d = 0.01
previous_error_x = 0
previous_error_y = 0

# Dimensions de l'image du tello edu
frame_width = 640  # 1280
frame_height = 480  # 720

# Initialisation des listes pour stocker les temps
cycle_times = []
inference_times = []

for i in range(50):
    start_time = time.time()
    image = frame_read.frame
    inference_start = time.time()
    result, coordinates, barycenter = detector.run_object_detection(image)  # Exécute la détection de personne sur l'image
    inference_end = time.time()

    # Enregistrer les temps
    inference_time = inference_end - inference_start
    inference_times.append(inference_time)

    if coordinates != [0, 0, 0, 0] and barycenter:  # si on détecte quelqu'un
        bx = barycenter[0]  # Coordonnée x du barycentre
        by = barycenter[1]  # Coordonnée y du barycentre

        # Calcul de la commande de rotation PID
        x_error = bx - frame_width // 2
        rotate_command = k_p * x_error + k_d * (x_error - previous_error_x)
        
        # Normalisation de la commande pour qu'elle soit entre 1 et 360 degrés
        rotate_command = max(1, min(360, int(abs(rotate_command))))

        if rotate_command > 0:
            if x_error > 0:
                tello.rotate_clockwise(rotate_command)
            else:
                tello.rotate_counter_clockwise(rotate_command)
        
        previous_error_x = x_error

    end = time.time()
    cycle_time = end - start_time
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
