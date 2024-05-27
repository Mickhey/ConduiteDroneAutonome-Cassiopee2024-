import person_detector_yolov8 as detectorv8 #Yolov8
import cv2
import time

# Chemin vers l'image de test
image_path = "/home/clem/Desktop/Casioppe/ConduiteDroneAutonome-Cassiopee2024-/Autonomous-Drone-Driving-ADD--main/kite.jpg"

# Charger l'image depuis le chemin spécifié
image = cv2.imread(image_path)

if image is None:
    print(f"Erreur: impossible de charger l'image à partir de {image_path}")
    exit()

# Nombre de tests d'inférence
num_tests = 100

# Fonction pour mesurer le temps d'inférence
def measure_inference_timev8(image):
    inference_times = []

    for _ in range(num_tests):
        start_time = time.time()
        result_image, coords, barycenter = detectorv8.run_object_detection(image)
        end_time = time.time()
        inference_times.append(end_time - start_time)

    avg_inference_time = sum(inference_times) / num_tests
    return avg_inference_time

avg_inference_timev8 = measure_inference_timev8(image)
#Resultat
print("Résultat : ", avg_inference_timev8)
