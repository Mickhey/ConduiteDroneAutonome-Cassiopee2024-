from djitellopy import Tello
import time
import person_detector_yolov8 as detector
import numpy as np
from threading import Thread, Condition

# Initialisation du drone
tello = Tello()
tello.connect()  # Connexion au drone Tello
print("Batterie:", tello.get_battery())  # Affichage du niveau de la batterie

tello.streamon()  # Activation du flux vidéo du drone
frame_read = tello.get_frame_read()  # Récupération de l'objet de lecture des images

tello.takeoff()  # Décollage du drone
stop_thread = False  # Variable pour contrôler l'arrêt des threads

# Paramètres PID initiaux
k_p = 0.1  # Gain proportionnel pour le contrôle PID
k_d = 0.01  # Gain dérivé pour le contrôle PID
previous_error_x = 0  # Erreur précédente sur l'axe X pour le contrôle PID

# Dimensions de l'image du Tello EDU
frame_width = 640  # Largeur de l'image du flux vidéo de base 1280 (natif sur le drone)
frame_height = 480  # Hauteur de l'image du flux vidéo de base 720

# Listes pour stocker les temps d'inférence et de cycle
inference_times = []
cycle_times = []
detection_results = []  # Liste pour stocker les résultats de détection
data_condition = Condition()  # Condition pour synchroniser les threads

# Fonction pour commander le drone en fonction des résultats de détection
def command_drone():
    global previous_error_x
    while not stop_thread:
        with data_condition:
            data_condition.wait(timeout=0.01)  # Attente d'une nouvelle détection ou d'un timeout
            if detection_results:
                # Récupération des coordonnées barycentriques de la détection
                bx, by = detection_results.pop(0)
                x_error = bx - frame_width // 2  # Calcul de l'erreur en X par rapport au centre de l'image

                # Calcul de la commande de rotation PID
                rotate_command = k_p * x_error + k_d * (x_error - previous_error_x)
                
                # Normalisation de la commande pour qu'elle soit entre 1 et 360 degrés
                rotate_command = max(1, min(360, int(abs(rotate_command))))

                # Commande de rotation du drone
                if x_error > 0:
                    tello.rotate_clockwise(rotate_command)
                else:
                    tello.rotate_counter_clockwise(rotate_command)
                
                previous_error_x = x_error  # Mise à jour de l'erreur précédente

# Fonction pour détecter les personnes à partir des images du drone
def detection_thread():
    while not stop_thread:
        start_time = time.time()  # Temps de début du cycle
        image = frame_read.frame  # Récupération de l'image actuelle du flux vidéo
        inference_start = time.time()  # Temps de début de l'inférence
        # Exécution de la détection d'objets (personnes) dans l'image
        result, coordinates, barycenter = detector.run_object_detection(image)
        inference_end = time.time()  # Temps de fin de l'inférence
        if coordinates != [0, 0, 0, 0] and barycenter:
            with data_condition:
                # Ajout des coordonnées barycentriques aux résultats de détection
                detection_results.append(barycenter)
                data_condition.notify()  # Notification du thread de commande
        # Stockage des temps d'inférence et de cycle
        inference_times.append(inference_end - inference_start)
        cycle_times.append(time.time() - start_time)

# Démarrage des threads de détection et de commande
detection_thread = Thread(target=detection_thread)
command_thread = Thread(target=command_drone)
detection_thread.start()
command_thread.start()

try:
    time.sleep(25)  # Temps de test (le drone fonctionne pendant 25 secondes à gerer autrement)
finally:
    stop_thread = True  # Arrêt des threads
    with data_condition:
        data_condition.notify_all()  # Notification pour libérer les threads en attente
    detection_thread.join()  # Attente de la fin du thread de détection
    command_thread.join()  # Attente de la fin du thread de commande
    tello.land()  # Atterrissage du drone
    tello.streamoff()  # Arrêt du flux vidéo
    tello.end()  # Déconnexion du drone

    # Calcul des moyennes des temps d'inférence et de cycle
    average_inference_time = np.mean(inference_times)
    average_cycle_time = np.mean(cycle_times)
    print(f"Moyenne du temps d'inférence: {average_inference_time:.3f} secondes")
    print(f"Moyenne du temps de cycle: {average_cycle_time:.3f} secondes")
