from djitellopy_optimized import Tello  # Bibliothèque optimisée
import time
import person_detector_yolov8 as detector
import numpy as np
from threading import Thread, Condition
import matplotlib.pyplot as plt
import datetime

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

tello.takeoff()
tello.move_up(50)

stop_thread = False

# Paramètres PID optimisés
k_px = 0.04  
k_dx = 0.07  
k_py = 0.12
k_dy = 0.08

previous_error_x = 0
previous_error_y = 0
x_err_sum = 0
y_err_sum = 0

# Dimensions de l'image
frame_width = 640
frame_height = 480

# Listes pour stocker les temps d'inférence et de cycle
inference_times = []
cycle_times = []
detection_results = []
data_condition = Condition()

def command_drone():
    global previous_error_x, x_err_sum, x_error
    while not stop_thread:
        with data_condition:
            data_condition.wait(timeout=0.01)
            if detection_results:
                bx, by = detection_results.pop(0)
                
                x_error = bx - frame_width // 2

                x_err_sum += x_error
                dx_err = x_error - previous_error_x
               
                rotate_command = k_px * x_error - k_dx * abs(dx_err)
                
                rotate_command = max(0, min(360, int(abs(rotate_command))))

                if abs(x_error) > 20:  # Augmentation du seuil pour éviter les petites corrections inutiles
                    tello.rotate(rotate_command if x_error > 0 else -rotate_command)

                previous_error_x = x_error

def detection_thread():
    while not stop_thread:
        global coordinates
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

detection_thread = Thread(target=detection_thread)
command_thread = Thread(target=command_drone)
detection_thread.start()
command_thread.start()

try:
    time.sleep(45)
finally:
    stop_thread = True
    with data_condition:
        data_condition.notify_all()
    detection_thread.join()
    command_thread.join()
    tello.land()
    tello.streamoff()
    print("Batterie:", tello.get_battery())
    tello.end()

    average_inference_time = np.mean(inference_times)
    average_cycle_time = np.mean(cycle_times)
    print(f"Moyenne du temps d'inférence: {average_inference_time:.3f} secondes")
    print(f"Moyenne du temps de cycle: {average_cycle_time:.3f} secondes")

    # Fin du profilage
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    profiling_filename = f"output_{timestamp}.prof"
    profiler.disable()
    profiler.dump_stats(profiling_filename)
