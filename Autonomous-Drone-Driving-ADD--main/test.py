from djitellopy import Tello
import cv2, math, time
import run_person_detector as detector
import numpy as np
import matplotlib.pyplot as plt


tello = Tello()
tello.connect()

print(tello.get_battery())

tello.streamon()
frame_read = tello.get_frame_read()

tello.takeoff()

tello.move_up(60) # s'élève de 60cm en plus pour être a hauteur humaine


for i in range (50): #boucle while meilleur mais flemme de traiter comment arreter la boucle

    image = frame_read.frame

    result, coordinates, barycenter = detector.run_object_detection(image) # Exécute la détection de personne sur l'image
    #print(coordinates, barycenter) # Affiche les coordonnées et le barycentre (optionnel, pratique pour debugage et tests)
    if (coordinates != [0,0,0,0]): #si on détecte qqn
        rapport = (coordinates[1] - coordinates[0]) / (coordinates[3] - coordinates[2])

        bx = barycenter[0] # Coordonnée x du barycentre
        by = barycenter[1] # Coordonnée y du barycentre
        
        

                # ==================== Algorithme de comportement du drone ===========
        
        if(bx > 448):
            #print("rotate right")
            tello.rotate_clockwise(10) 
        elif(bx < 408):
            #print("rotate left")
            tello.rotate_counter_clockwise(10)  
        
        # LIGNES SUIVANTES A TESTER 
        #elif (rapport >= 2 and by < 220):
        #    print("move frontward")
        #    tello.move_forward(20) 
        elif (by > 260):
            print("move backward")
            tello.move_back(20) 
    
    #key = cv2.waitKey(1) # Ajoute un petit délai pour permettre à l'interface graphique de se mettre à jour
    #cv2.imshow("Drone tracking",image) si vous arrivez a faire marcher cv2.imshow



tello.land()
tello.streamoff()

tello.end()
                