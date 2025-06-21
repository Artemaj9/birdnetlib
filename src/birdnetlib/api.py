from fastapi import FastAPI
from pydantic import BaseModel
from birdnetlib.analyzer import Analyzer
from birdnetlib.recording import Recording
import base64
import tempfile

app = FastAPI()

analyzer = Analyzer(
    model_path="./models/lite/BirdNET_6K_GLOBAL_MODEL.tflite",
    label_path="./models/lite/labels.txt"
)

class PredictRequest(BaseModel):
    audio: str
    lat: float = 48.8566
    lon: float = 2.3522
    week: int = 30

@app.post("/api/predict")
async def predict(req: PredictRequest):
    # Save audio file from base64 string
    audio_bytes = base64.b64decode(req.audio)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        tmp.flush()

        recording = Recording(
            analyzer,
            tmp.name,
            lat=req.lat,
            lon=req.lon,
            week=req.week
        )
        recording.analyze()

        results = [
            {"species": d["common_name"], "confidence": d["confidence"]}
            for d in recording.detections
        ]

        return {"predictions": results}

