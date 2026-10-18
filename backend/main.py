from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Folder paths (work no matter where you start the server from)
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.joblib"
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Water Potability Predictor")

# Load the trained model once, when the server starts
model = joblib.load(MODEL_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# What the website must send us (with basic validation)
class WaterInput(BaseModel):
    ph: float = Field(ge=0, le=14)
    hardness: float = Field(ge=0)
    solids: float = Field(ge=0)
    turbidity: float = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: WaterInput):
    # Column names must match the ones used in train.py
    row = pd.DataFrame([{
        "ph": data.ph,
        "Hardness": data.hardness,
        "Solids": data.solids,
        "Turbidity": data.turbidity,
    }])

    pred = int(model.predict(row)[0])
    prob = float(model.predict_proba(row)[0][pred])

    return {
        "result": "Potable" if pred == 1 else "Not Potable",
        "confidence": round(prob * 100, 1),
        "disclaimer": (
            "This is only an estimate. Laboratory testing is required "
            "to confirm whether water is safe to drink."
        ),
    }


# Serve the website from the same server (must stay at the bottom)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")