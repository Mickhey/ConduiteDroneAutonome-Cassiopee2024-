from djitellopy import Tello
import time
import person_detector_yolov8 as detector
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Profilage
import cProfile

# Profiler le script entier
profiler = cProfile.Profile()
profiler.enable()

# Initialisation du drone
tello = Tello()
tello.connect()  # Connexion au drone Tello
print("Batterie:", tello.get_battery())  # Affichage du niveau de la batterie

tello.streamon()  # Activation du flux vidéo du drone
frame_read = tello.get_frame_read()  # Récupération de l'objet de lecture des images

tello.takeoff()  # Décollage du drone
tello.move_up(50)

# Paramètres PID initiaux
k_px = 0.03 # Gain proportionnel pour le contrôle PID optimal à 0.08 / 0.09 / 0.03
k_dx = 0.09 # Gain dérivé pour le contrôle PID optimal à 0.06 / 0.09 / 0.09
# k_ix = 0.002 en pratique l'intégrateur mène à des instabilités

k_py = 0.1 # Gain proportionnel pour le contrôle PID optimal à 0.08 / 0.09 / 0.03
k_dy = 0.1 # Gain dérivé pour le contrôle PID optimal à 0.06 / 0.09 / 0.09

previous_error_x = 0  # Erreur précédente sur l'axe X pour le contrôle PID
previous_error_y = 0  # Erreur précédente sur l'axe Y pour le contrôle PID
x_err_sum = 0  # Erreur sommée pour l'intégrateur axe X rotation 
y_err_sum = 0  # Erreur sommée pour l'intégrateur axe Y translation 

# Toutes les listes pour stocker chaque type d'erreur
xerrsl = [] # Erreur sommée 
xerrl = []  # Erreur courante
derrl = []  # Erreur dérivée 

# Dimensions de l'image du Tello EDU
frame_width = 640  # Largeur de l'image du flux vidéo de base 1280 (natif sur le drone)
frame_height = 480  # Hauteur de l'image du flux vidéo de base 720

# Listes pour stocker les temps d'inférence et de cycle
inference_times = []
cycle_times = []
start_time = time.time()
try:
    while time.time() - start_time < 45 :
        cycle_start_time = time.time()  # Début du cycle

        # Récupération de l'image actuelle du flux vidéo
        image = frame_read.frame  

        # Détection des personnes dans l'image
        inference_start_time = time.time()  # Début de l'inférence
        result, coordinates, barycenter = detector.run_object_detection(image)
        inference_end_time = time.time()  # Fin de l'inférence

        if coordinates != [0, 0, 0, 0] and barycenter:
            bx, by = barycenter
            rapport = (coordinates[1] - coordinates[0]) / (coordinates[3] - coordinates[2])
            
            x_error = bx - frame_width // 2  # Erreur en X par rapport au centre de l'image
            y_error = by - frame_height // 2

            x_err_sum += x_error
            dx_err = x_error - previous_error_x

            y_err_sum += y_error
            dy_err = y_error - previous_error_y

            # Commande de rotation PID
            rotate_command = k_px * x_error - k_dx * abs(dx_err)
            pid_out_y = k_py * y_error - k_dy * abs(dy_err)
            
            # Normalisation de la commande
            rotate_command = max(0, min(360, int(abs(rotate_command))))

            # Commande de rotation du drone
            if x_error > 0:
                tello.rotate_clockwise(rotate_command)
            elif x_error < 0:
                tello.rotate_counter_clockwise(rotate_command)
            
            xerrl.append(x_error)
            xerrsl.append(x_err_sum)
            derrl.append(dx_err)
            
            previous_error_x = x_error  # Mise à jour de l'erreur précédente en X
            previous_error_y = y_error  # Mise à jour de l'erreur précédente en Y

        # Stockage des temps d'inférence et de cycle
        inference_times.append(inference_end_time - inference_start_time)
        cycle_times.append(time.time() - cycle_start_time)

finally:
    tello.land()  # Atterrissage du drone
    tello.streamoff()  # Arrêt du flux vidéo
    print("Batterie:", tello.get_battery())  # Affichage du niveau de la batterie
    print("x_err_sum =", x_err_sum)
    print("x_error =", x_error)
    print("previous error x =", previous_error_x)
    '''
    # Tracer toutes les erreurs
    plt.plot(xerrl)
    plt.title("Erreur courante")
    plt.show()
    plt.plot(xerrsl)
    plt.title("Erreurs sommées")
    plt.show()
    plt.plot(derrl)
    plt.title("Erreur dérivée")
    plt.show()
    '''
    tello.end()  # Déconnexion du drone

    # Calcul des moyennes des temps d'inférence et de cycle
    average_inference_time = np.mean(inference_times)
    average_cycle_time = np.mean(cycle_times)
    print(rapport)
    print(f"Moyenne du temps d'inférence: {average_inference_time:.3f} secondes")
    print(f"Moyenne du temps de cycle: {average_cycle_time:.3f} secondes")


    # Fin du profilage
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    profiling_filename = f"output_{timestamp}.prof"
    profiler.disable()
    profiler.dump_stats(profiling_filename)
