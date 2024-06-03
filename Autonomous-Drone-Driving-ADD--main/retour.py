import person_detector_yolov8 as detectorv8  # Yolov8
import cv2
import numpy as np

# Chemin vers l'image de test
image_path = "/home/clem/Downloads/IMG_20240603_155246.jpg"

# Charger l'image depuis le chemin spécifié
original_image = cv2.imread(image_path)

if original_image is None:
    print(f"Erreur: impossible de charger l'image à partir de {image_path}")
    exit()

# Exécuter une seule inférence en utilisant votre fonction
resized_image_pil, coords, barycenter = detectorv8.run_object_detection(original_image)

# Convertir l'image redimensionnée de PIL à NumPy
resized_image = np.array(resized_image_pil)

# Dessiner la boîte et le barycentre sur l'image redimensionnée
if coords and len(coords) == 4:
    x_min, y_min, x_max, y_max = coords
    if (x_max - x_min) > 0 and (y_max - y_min) > 0:
        cv2.rectangle(resized_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 4)

if barycenter and len(barycenter) == 2:
    x, y = barycenter
    if x > 0 and y > 0:
        cv2.circle(resized_image, (x, y), 10, (0, 0, 255), -1)

# Enregistrer l'image redimensionnée et modifiée
output_image_path = "/home/clem/Desktop/Casioppe/ConduiteDroneAutonome-Cassiopee2024-/Autonomous-Drone-Driving-ADD--main/kite_with_box.jpg"
cv2.imwrite(output_image_path, cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR))

# Résultat
print(f"Image modifiée enregistrée à {output_image_path}")
