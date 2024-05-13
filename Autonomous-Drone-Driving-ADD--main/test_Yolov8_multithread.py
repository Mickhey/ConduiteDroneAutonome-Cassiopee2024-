from djitellopy import Tello
import time
import person_detector_yolov8 as detector
import numpy as np
from threading import Thread, Condition

# Initialisation du drone
tello = Tello()
tello.connect()
print("Batterie:", tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()
stop_thread = False

# Paramètres PID initiaux
k_p = 0.1
k_d = 0.01
previous_error_x = 0
previous_error_y = 0

# Dimensions de l'image du tello edu
frame_width = 640 #1280
frame_height = 480 #720

inference_times = []
cycle_times = []
detection_results = []
data_condition = Condition()

def command_drone():
    global previous_error_x, previous_error_y
    while not stop_thread:
        with data_condition:
            data_condition.wait(timeout=1)  
            if detection_results:
                bx, by = detection_results.pop(0)
                x_error = bx - frame_width // 2

                # Calcul de la commande de rotation PID
                rotate_command = k_p * x_error + k_d * (x_error - previous_error_x)
                
                # Normalisation de la commande pour qu'elle soit entre 1 et 360 degrés
                rotate_command = max(1, min(360, int(abs(rotate_command))))

                if rotate_command > 0:
                    if x_error > 0:
                        tello.rotate_clockwise(rotate_command)
                    else:
                        tello.rotate_counter_clockwise(rotate_command)
                
                previous_error_x = x_error


def detection_thread():
    while not stop_thread:
        start_time = time.time()
        image = frame_read.frame
        inference_start = time.time()
        result, coordinates, barycenter = detector.run_object_detection(image)
        inference_end = time.time()
        if coordinates != [0, 0, 0, 0] and barycenter:
            with data_condition:
                detection_results.append(barycenter)
                data_condition.notify()
        inference_times.append(inference_end - inference_start)
        cycle_times.append(time.time() - start_time)

# Démarrage des threads de détection et de commande
detection_thread = Thread(target=detection_thread)
command_thread = Thread(target=command_drone)
detection_thread.start()
command_thread.start()


try:
    time.sleep(25) #Temps de test
finally:
    stop_thread = True
    with data_condition:  
        data_condition.notify_all()
    detection_thread.join()
    command_thread.join()
    tello.land()
    tello.streamoff()
    tello.end()

    # Calcul des moyennes
    average_inference_time = np.mean(inference_times)
    average_cycle_time = np.mean(cycle_times)
    print(f"Moyenne du temps d'inférence: {average_inference_time:.3f} secondes")
    print(f"Moyenne du temps de cycle: {average_cycle_time:.3f} secondes")

