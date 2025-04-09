import logging

import cv2
import numpy as np
import torch
from facenet_pytorch import MTCNN
from PIL import Image
from tensorflow.keras.models import load_model
import os

from ..config import *

logger = logging.getLogger(PROJECT_NAME)


class FaceEmotionRecognition:
    def __init__(self):
        self.mtcnn = MTCNN(keep_all=True, device="cuda" if torch.cuda.is_available() else "cpu")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "best_model.keras")
        MODEL_PATH = os.path.normpath(MODEL_PATH)
        logger.info(f"Model path: {MODEL_PATH}")
        self.model = load_model(MODEL_PATH)
        self.label_map = {
            0: "angry",
            1: "disgust",
            2: "fear",
            3: "happy",
            4: "sad",
            5: "surprise",
            6: "neutral",
        }

    def detect_emotions(self, img_path):
        try:
            # Load image
            if isinstance(img_path, str):
                img_pil = Image.open(img_path).convert("RGB")
            else:
                img_pil = Image.fromarray(img_path).convert("RGB")

            img_cv = np.array(img_pil)
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2BGR)

            # Detect faces
            boxes, probs = self.mtcnn.detect(img_pil)

            if boxes is None or len(boxes) == 0:
                return "No face detected", []

            response = []

            for box, prod in zip(boxes, probs):
                if prod < 0.9:
                    continue
                
                x1, y1, x2, y2 = map(int, box)
                x1, y1 = max(0, x1), max(0, y1)
                w, h = x2 - x1, y2 - y1

                # Crop and preprocess
                face_crop = img_cv[y1 : y1 + h, x1 : x1 + w]
                face_resized = cv2.resize(face_crop, (48, 48))
                face_norm = face_resized / 255.0
                face_input = np.expand_dims(face_norm, axis=0)

                # Predict
                preds = self.model.predict(face_input, verbose=0)[0]
                class_id = np.argmax(preds)
                confidence = float(np.max(preds))
                emotion = self.label_map.get(class_id, "Unknown")

                response.append(
                    {
                        "bbox": [x1, y1, w, h],
                        "emotion": emotion,
                        "confidence": confidence,
                    }
                )

            return "Succeed to detect emotion", response

        except Exception as e:
            logger.error(f"Emotion analysis failed: {str(e)}")
            return str(e), []
