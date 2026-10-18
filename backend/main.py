from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "model.joblib"
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="Water Potability Predictor")
model = joblib.load(MODEL_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class WaterInput(BaseModel):
    ph: float = Field(ge=0, le=14)
    hardness: float = Field(ge=0)
    solids: float = Field(ge=0)
    chloramines: float = Field(ge=0)
    sulfate: float = Field(ge=0)
    conductivity: float = Field(ge=0)
    organic_carbon: float = Field(ge=0)
    trihalomethanes: float = Field(ge=0)
    turbidity: float = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: WaterInput):
    # Column names must match train.py exactly
    row = pd.DataFrame([{
        "ph": data.ph,
        "Hardness": data.hardness,
        "Solids": data.solids,
        "Chloramines": data.chloramines,
        "Sulfate": data.sulfate,
        "Conductivity": data.conductivity,
        "Organic_carbon": data.organic_carbon,
        "Trihalomethanes": data.trihalomethanes,
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


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")