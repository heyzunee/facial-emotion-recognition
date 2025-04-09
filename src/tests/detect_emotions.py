import cv2

from ..config import *
from ..module.detector import FaceEmotionRecognition

img_path = "datasets/test/3.jpg"

detector = FaceEmotionRecognition()
message, results = detector.detect_emotions(img_path=img_path)

image = cv2.imread(img_path)
for result in results:
    print(result)
    x, y, w, h = result["bbox"]
    emotion = result["emotion"]
    confidence = result["confidence"]

    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 10)

    label = f"{emotion} ({confidence:.2f})"
    cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 5)
    print("Added bounding box on image.")

cv2.imwrite(f"{img_path.split('.')[0]}_output.jpg", image)
