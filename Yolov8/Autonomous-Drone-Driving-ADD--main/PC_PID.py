from djitellopy_optimized import Tello  # Bibliothèque optimisée
import time
import person_detector_yolov8 as detector
import numpy as np
from threading import Thread, Condition
import matplotlib.pyplot as plt
import datetime
import cv2


# Initialisation du drone
tello = Tello()
tello.connect()
print("Batterie:", tello.get_battery())
tello.set_video_fps(Tello.FPS_5)
tello.set_video_bitrate(Tello.BITRATE_5MBPS)
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

                if abs(x_error) > 80:  # Augmentation du seuil pour éviter les petites corrections inutiles
                    #print("rotate", rotate_command)
                    tello.rotate(rotate_command if x_error > 0 else -rotate_command)
                    
                #les lignes suivantes sont à commenter si on veut éviter les translations
                else:
                    rapport = (coordinates[1] - coordinates[3]) / (coordinates[0] - coordinates[2])
                #    print(by)
                #    print(rapport)
                    if (rapport >= 2.5 and by >=180 ):
                        #print("move forward")
                        tello.move_forward(30)
                        
                    elif (rapport <= 1.7):
                        #print("move backwards")
                        tello.move_back(30)




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
        base_width = 640  # Largeur cible (hauteur de 480)
        w_percent = (base_width / float(image.shape[1]))
        h_size = int((float(image.shape[0]) * float(w_percent)))
        image = cv2.resize(image, (base_width, h_size), interpolation=cv2.INTER_LINEAR)
        image = cv2.circle(image,barycenter, 5, (0, 0, 255),-1)
        image = cv2.rectangle(image,(coordinates[0],coordinates[1]),(coordinates[2],coordinates[3]),(255,0,0),3)
        cv2.imshow("result",image)
        cv2.waitKey(1)

detection_thread = Thread(target=detection_thread)
command_thread = Thread(target=command_drone)
detection_thread.start()
command_thread.start()

try:
    #pour augmenter le temps de démo
    time.sleep(60)
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
 
