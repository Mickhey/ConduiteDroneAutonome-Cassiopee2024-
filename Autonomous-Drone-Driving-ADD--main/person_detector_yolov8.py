from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import torch

D = 0 #O pour GPU 1(si dispo) pour CPU
if(D==0):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
else:
    device = 'cpu'

print(f"Utilisation de {device} pour le traitement.")

#On charge le modèle (ici général entrainer sur coco 80 classes)
model = YOLO('yolov8n.pt')


def run_object_detection(image):

     # Redimensionner l'image pour réduire la résolution
    base_width = 640  # Largeur cible (hauteur de 480)
    w_percent = (base_width / float(image.shape[1]))
    h_size = int((float(image.shape[0]) * float(w_percent)))
    image = cv2.resize(image, (base_width, h_size), interpolation=cv2.INTER_LINEAR)


    # Convertir l'image en format compatible pour YOLOv8
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    # Exécuter l'inférence en spécifiant 'classes=0' pour détecter uniquement les personnes et non les auters classes et on limite a une detection
    results = model.predict(image,classes=0,max_det=1,verbose=False,device=device)

     # Extraire la detection, la boite puis ces coordonnées pour calculer le barycentre
    if results[0].boxes and len(results[0].boxes) > 0:

        box = results[0].boxes[0] 
        x1, y1, x2, y2 = map(int,box.xyxy[0])#Converti le tensor pour acceder au valeurs
        coordinates = [x1, y1, x2, y2]
        barycenter = [(x1 + x2) // 2, (y1 + y2) // 2]
    else:
        coordinates = [0, 0, 0, 0]
        barycenter = [0, 0]

    # Convertir l'image pour l'affichage si nécessaire
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    return image, coordinates, barycenter

