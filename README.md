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

- The model is fine-tuned based on **VGG19** architecture.
- Fine-tuning and training notebook can be found at: `src/model/Fine_tuning_VGG_19_for_FER.ipynb`
- The model demonstrates high performance on emotion classification tasks.

---

## Installation & Running the API

### Step 1: Download Pretrained Model

- Download the pretrained model from this link: 👉 [Download model](https://drive.google.com/file/d/1r70CDOi8aIQCAI9DmS-YlgDEBdFR4Iua/view?usp=drive_link)
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

---
### Step 4: Test API with curl
```bash
curl -X POST http://localhost:9000/emotion \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/your_path/src/datasets/test/3.jpg"
```