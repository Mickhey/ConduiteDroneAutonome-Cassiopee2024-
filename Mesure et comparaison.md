# Rapport de Performance YOLOv8

Paramètre de base, 640*480 avec le GPU

## YOLOv8 GPU avec `test_inference_GPU_CPU.py`

### Résultats pour 100 inférences

- Résultat 1 : 0.0243162202835083 secondes par image
- Résultat 2 : 0.02499863624572754 secondes par image
- Résultat 3 : 0.026942615509033204 secondes par image

### Résultat pour 1000 inférences

- Résultat unique : 0.010336869716644288 secondes par image

## YOLOv8 CPU avec `test_inference_GPU_CPU.py`

### Résultats pour 100 inférences 

- Résultat 1 : 0.08048184156417847 secondes par image
- Résultat 2 : 0.05577165603637695 secondes par image
- Résultat 3 : 0.05577165603637695 secondes par image

### Résultat pour 1000 inférences

- Résultat unique : 0.046849696874618534 secondes par image

## Conclusion GPU vs CPU

Les calculs sont beaucoup plus stables et rapides sur le GPU, tandis que les calculs sont plus longs et moins stables sur le CPU.

## Résolution native du Tello (1280x720) avec GPU

### Résultats pour 100 inférences

- Résultat 1 : 0.041743247509002684 secondes par image
- Résultat 2 : 0.03516468763351441 secondes par image
- Résultat 3 : 0.0360118794441223 secondes par image

### Résultat pour 1000 inférences

- Résultat unique : 0.020993482112884522 secondes par image

## Résolution utilisée (640x480) avec GPU

### Résultats pour 1000 inférences

- Résultat unique : 0.01076058554649353 secondes par image

### Résultats pour 100 inférences

- Résultat 1 : 0.026055560111999512 secondes par image
- Résultat 2 : 0.024811456203460692 secondes par image
- Résultat 3 : 0.026187307834625244 secondes par image
  
## Conclusion Résolution

On remarque bien que l'utilisation d'une résolution plus basse réduit le temps d'inférence, 640*480 nous permet de réduire le temps d'inférence tout en gardant une précision satisfaisante

## Comparaison entre YOLOv4 et YOLOv8

### Latence

- **YOLOv4** : La latence typique pour YOLOv4 sur un GPU moderne (comme le NVIDIA V100) est d'environ 12 à 15 ms par image.
- **YOLOv8** : YOLOv8 offre une latence réduite, environ 7 à 10 ms par image sur des GPUs modernes comme le NVIDIA A100.

#### Précision (mAP)

- **YOLOv4** : YOLOv4 atteint environ 43-44% de mAP sur le benchmark COCO.
- **YOLOv8** : YOLOv8 améliore cette précision avec un mAP de 50-52% sur le benchmark COCO, grâce à des améliorations architecturales et des techniques de formation plus avancées.

### Conclusion

Pour la détection en temps réel de personnes avec un drone, **YOLOv8** est le choix recommandé. Il offre une meilleure précision et une latence plus faible par rapport à YOLOv4, ce qui est crucial pour les applications en temps réel nécessitant des réponses rapides et fiables.

## Sources

- [Ultralytics](https://docs.ultralytics.com/)
- [A Comprehensive Review of YOLO Architectures in Computer Vision: From YOLOv1 to YOLOv8 and YOLO-NAS](https://arxiv.org/abs/2304.00501)
- [Roboflow yolov4 vs yolov8](https://roboflow.com/compare/yolov8-vs-yolov4-tiny)