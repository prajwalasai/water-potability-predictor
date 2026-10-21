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


def safety_check(d: WaterInput):
    """Rule-based check against drinking water standard limits."""
    reasons = []
    if d.ph < 6.5 or d.ph > 8.5:
        reasons.append(f"pH {d.ph} is outside the acceptable range of 6.5 to 8.5")
    if d.hardness > 600:
        reasons.append(f"Hardness {d.hardness} mg/L is above the limit of 600 mg/L")
    if d.solids > 2000:
        reasons.append(f"Solids (TDS) {d.solids} ppm is above the limit of 2000 ppm")
    if d.chloramines > 4:
        reasons.append(f"Chloramines {d.chloramines} ppm is above the limit of 4 ppm")
    if d.sulfate > 400:
        reasons.append(f"Sulfate {d.sulfate} mg/L is above the limit of 400 mg/L")
    if d.trihalomethanes > 80:
        reasons.append(f"Trihalomethanes {d.trihalomethanes} µg/L is above the limit of 80 µg/L")
    if d.turbidity > 5:
        reasons.append(f"Turbidity {d.turbidity} NTU is above the limit of 5 NTU")
    return reasons


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: WaterInput):
    disclaimer = (
        "This is only an estimate. Laboratory testing is required "
        "to confirm whether water is safe to drink."
    )

    # Step 1: safety rules
    reasons = safety_check(data)
    if reasons:
        return {
            "result": "Not Potable",
            "confidence": None,
            "method": "Standard limits check",
            "reasons": reasons,
            "disclaimer": disclaimer,
        }

    # Step 2: machine learning model
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
        "method": "Machine learning model (all values within standard limits)",
        "reasons": [],
        "disclaimer": disclaimer,
    }


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")