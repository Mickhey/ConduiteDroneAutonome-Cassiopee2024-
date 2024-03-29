from djitellopy import Tello
import cv2, math, time
import run_person_detector as detector
import numpy as np
from threading import Thread




tello = Tello()
tello.connect()

tello.streamon()


tello.takeoff()

tello.move_up(50)

def action(tello):
    frame_read = tello.get_frame_read()
    img = frame_read.frame
    while True:
        result, coordinates, barycenter = detector.run_object_detection(img)
        if (coordinates != [0,0,0,0]):
            
            bx = barycenter[0] # Coordonnée x du barycentre
            by = barycenter[1] # Coordonnée y du barycentre

            rapport = (coordinates[1] - coordinates[0]) / (coordinates[3] - coordinates[2]) # Calcul rapport longueur / largeur avec les coordonnées du rectangle de détection
            #print(rapport) #affichache du rapport l/L (optionnel)

                # ==================== Algorithme de comportement du drone ===========
         
            if(bx > 448):
                print("rotate right")
                tello.rotate_clockwise(10) 
            elif(bx < 408):
                print("rotate left")
                tello.rotate_counter_clockwise(10)  
            #elif (rapport >= 2 and by < 220):
            #    print("move frontward")
            #    tello.move_forward(15) # translation de 15 cm vers l'avant

            #elif (by > 260):
            #    print("move backward")
            #    tello.move_back(15) # translation de 15 cm vers l'arrière
        
        #cv2.imshow("Image", result.astype(np.uint8)) 
        key = cv2.waitKey(1) # Ajoute un petit délai pour permettre à l'interface graphique de se mettre à jour


thread = Thread(target=action(tello))


time.sleep(20)

tello.land()

tello.streamoff()
tello.end()

                