from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Run inference on 'bus.jpg' with arguments
model.predict('/home/clem/Desktop/Casioppe/Image_Test/1.jpg',classes=0)