  # 🎭 Face Emotion Recognition API

A Python-based API for facial emotion recognition from images containing one or multiple human faces.

---

## API Features

- **Endpoint**: `POST /emotion`
- **Request Input**: A single image file (`.jpg` or `.png`) submitted as `multipart/form-data`.
- **Response Output**: JSON object with a list of detected faces, each including:
  - `bounding_box`: coordinates and size of the face (x, y, width, height)
  - `emotion`: one of the predefined emotions
    - `"happy"`, `"sad"`, `"angry"`, `"fear"`, `"surprise"`, `"neutral"`
  - `confidence`: score from `0` to `1` representing model certainty

---

## Model Information

### Face Detection
- **Model used**: `Haar Cascade Classifier` from OpenCV.
- This lightweight model efficiently detects multiple faces in an image.

### Face Emotion Recognition
- **Base model**: `VGG19` pretrained on ImageNet.
- **Fine-tuning strategy**:
  - Replaced the final classifier layers of VGG19 with emotion-specific fully connected layers.
  - Fine-tuned on the **FER2013** dataset (Facial Expression Recognition 2013).
  - Used data augmentation (rotation, zoom, shift) to enhance generalization.
- **Performance**:
  - Validation Accuracy: **~72.3%**
  - Inference Time: ~45ms per face on CPU.

Fine-tuning and training notebook can be found at: `src/model/Fine_tuning_VGG_19_for_FER.ipynb`

---

## Installation & Running the API

### Step 1: Download Pretrained Model

- Download the pretrained model from this link: [Pretrained Model](https://drive.google.com/file/d/1r70CDOi8aIQCAI9DmS-YlgDEBdFR4Iua/view?usp=drive_link)
- Place the downloaded model file inside the `src/model` directory.

---

### Step 2: Build Docker Image

```bash
docker build -t detect_emotions:v1 .
```
---

### Step 3: Run Docker Container
```bash
docker run -it -p 9000:9000 detect_emotions:v1
```
The API will be available at: http://localhost:9000/emotion

---

### Step 4: Test API with curl
```bash
curl -X POST http://localhost:9000/emotion \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/your_path/src/datasets/test/3.jpg"
```
Sample response:
```bash
[
  {
    "bounding_box": [120, 85, 90, 90],
    "emotion": "happy",
    "confidence": 0.94
  },
  {
    "bounding_box": [260, 100, 85, 85],
    "emotion": "neutral",
    "confidence": 0.88
  }
]
```
