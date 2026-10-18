# 💧 Water Potability Predictor

A web app that uses machine learning to estimate whether drinking water is
**Potable** or **Not Potable** from water quality measurements.

> ⚠️ **Important:** The prediction is only an estimate, not a guarantee that
> water is safe. Laboratory testing is required to confirm actual water safety.


## Problem
People often cannot tell whether their drinking water is safe, and laboratory
testing is not always immediately accessible. This project explores how machine
learning can give a quick, preliminary estimate from measured parameters.

## How it works
1. The user enters pH, hardness, solids (TDS) and turbidity.
2. The frontend sends the values to the backend.
3. The backend runs them through a trained Random Forest model.
4. The website shows Potable / Not Potable, the model's confidence, and a
   reminder that lab testing is needed.

## Tech stack
- **Model:** Python, pandas, scikit-learn (Random Forest)
- **Backend:** FastAPI + Uvicorn
- **Frontend:** HTML, CSS, JavaScript

## Project structure
```
water-potability-predictor/
├── data/water_potability.csv
├── model/train.py, model.joblib
├── backend/main.py
├── frontend/index.html, style.css, script.js
└── requirements.txt
```

## Run locally
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python model/train.py
uvicorn backend.main:app --reload
```
Then open http://127.0.0.1:8000

## Model results
- Dataset: public Kaggle "Water Potability" dataset (3,276 samples)
- Inputs used: pH, Hardness, Solids, Turbidity
- Test accuracy: [your accuracy]
- Precision / recall: [your numbers from train.py output]

## Limitations
- The dataset is not from Warangal, so results cannot be assumed to apply to
  local water sources.
- Only four parameters are used. Real safety also depends on bacteria,
  chemicals and heavy metals that are not measured here.
- The dataset is small and noisy, so accuracy is moderate.

## Future work
- Collect lab-verified water samples from Warangal and retrain the model.
- Validate the model locally before any real-world use.
- Add more parameters (for example chloramines, sulfate, conductivity).

## Author
macherla prajwala sai