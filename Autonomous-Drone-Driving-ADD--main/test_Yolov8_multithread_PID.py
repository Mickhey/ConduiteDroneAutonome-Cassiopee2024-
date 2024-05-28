from djitellopy import Tello
import time
import person_detector_yolov8 as detector
import numpy as np
from threading import Thread, Condition
import matplotlib.pyplot as plt

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

stop_thread = False  # Variable pour contrôler l'arrêt des threads

# Paramètres PID initiaux
k_px = 0.03 # Gain proportionnel pour le contrôle PID optimal à 0.08 / 0.09 / 0.03
k_dx = 0.09 # Gain dérivé pour le contrôle PID optimal à 0.06 / 0.09 / 0.09
# k_ix = 0.002 en pratique l'intégrateur mène à des instabilités

k_py = 0.1 # Gain proportionnel pour le contrôle PID optimal à 0.08 / 0.09 / 0.03
k_dy = 0.1 # Gain dérivé pour le contrôle PID optimal à 0.06 / 0.09 / 0.09


previous_error_x = 0  # Erreur précédente sur l'axe X pour le contrôle PID
previous_error_y = 0  # Erreur précédente sur l'axe X pour le contrôle PID
x_err_sum = 0  # erreur sommée pour l'intégrateur axe X rotation 
y_err_sum = 0  #  erreur sommée pour l'intégrateur axe Y translation 

# toutes les listes pour stocker chaque type d'erreur
xerrsl = [] # erreur sommée 
xerrl = []  # erreur courante
derrl = []  # erreur dérivée 

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
    global previous_error_x,x_err_sum,x_error,previous_error_y,y_err_sum,y_error,rapport
    while not stop_thread:
        with data_condition:
            data_condition.wait(timeout=0.01)  # Attente d'une nouvelle détection ou d'un timeout
            if detection_results:
                # Récupération des coordonnées barycentriques de la détection
                bx, by = detection_results.pop(0)
                rapport = (coordinates[1] - coordinates[0]) / (coordinates[3] - coordinates[2])
                
                x_error = bx - frame_width // 2  # Calcul de l'erreur en X par rapport au centre de l'image
                y_error = by - frame_height // 2


                x_err_sum += x_error
                dx_err = x_error - previous_error_x #erreur précédente ( ou dérivée)

                y_err_sum += y_error
                dy_err = y_error - previous_error_y


                # Calcul de la commande de rotation PID
                rotate_command = k_px * x_error - k_dx * abs(dx_err)

                pid_out_y = k_py * y_error - k_dy * abs(dy_err)
                
                # Normalisation de la commande pour qu'elle soit entre 0 et 360 degrés
                rotate_command = max(0, min(360, int(abs(rotate_command))))

                # Commande de rotation du drone
                if x_error > 0:  # ajout éventuel de la condition "and dx_err > 100 "
                    tello.rotate_clockwise(rotate_command)
                elif x_error < 0: # ajout éventuel de la condition "and dx_err < -100 "
                    tello.rotate_counter_clockwise(rotate_command)
                '''
                # rapport modifié mais globalement le déplacement avant arrière est à revoir
                if rapport >= 2.2 and abs(x_error)<=150:  # ajout de la condition abs(x_error)<=150 pour empecher le drone d'avancer ou reculer s'il n'est pas déjà centré horizontalement sur la personne, ajout éventuel de "and abs(x_err_sum)<= 1000"
                    if y_error>0:
                        tello.move_forward(max(20,int(abs(pid_out_y))))
                    if y_error < 0:
                        tello.move_back(max(20,int(abs(pid_out_y))))
                '''
                xerrl.append(x_error)
                xerrsl.append(x_err_sum)
                derrl.append(dx_err)
                
                previous_error_x = x_error  # Mise à jour de l'erreur précédente en x
                previous_error_y = y_error  # Mise à jour de l'erreur précédente en y


# Fonction pour détecter les personnes à partir des images du drone
def detection_thread():
    while not stop_thread:
        global coordinates
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
    time.sleep(20)  # Temps de test (le drone fonctionne pendant 25 secondes à gerer autrement)
finally:
    stop_thread = True  # Arrêt des threads
    with data_condition:
        data_condition.notify_all()  # Notification pour libérer les threads en attente
    detection_thread.join()  # Attente de la fin du thread de détection
    command_thread.join()  # Attente de la fin du thread de commande
    tello.land()  # Atterrissage du drone
    tello.streamoff()  # Arrêt du flux vidéo
    print("Batterie:", tello.get_battery())  # Affichage du niveau de la batterie
    print("x_err_sum =",x_err_sum)
    print("x_error =",x_error)
    print("previous error x =",previous_error_x)
    '''
    # tracer toutes les erreurs , il faut que les courbes tendent vers 0 idéalement
    plt.plot(xerrl)
    plt.title("erreur courante")
    plt.show()
    plt.plot(xerrsl)
    plt.title("erreurs sommées")
    plt.show()
    plt.plot(derrl)
    plt.title("erreur dérivée")
    plt.show()
    '''
    tello.end()  # Déconnexion du drone

    # Calcul des moyennes des temps d'inférence et de cycle
    average_inference_time = np.mean(inference_times)
    average_cycle_time = np.mean(cycle_times)
    print(rapport)
    print(f"Moyenne du temps d'inférence: {average_inference_time:.3f} secondes")
    print(f"Moyenne du temps de cycle: {average_cycle_time:.3f} secondes")

    # Fin profilage
    profiler.disable()
    profiler.dump_stats("output.prof")