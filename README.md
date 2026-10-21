# 💧 Water Potability Predictor

A web application that estimates whether drinking water is **Potable** or **Not Potable** from nine water quality measurements. It combines a drinking-water standards check with a machine learning model.

> ⚠️ The prediction is only an estimate, not a guarantee that water is safe. Laboratory testing is required to confirm actual water safety.

## Problem
People often cannot tell whether their drinking water is safe, and laboratory testing is not always immediately accessible. This project explores how machine learning, together with known quality limits, can give a quick preliminary estimate. It is a prototype for a potential application in Warangal.

## How it works
1. The user opens the website and enters nine water quality values.
2. The frontend sends the values to the backend.
3. **Step 1, safety rules:** the backend compares the values with drinking-water limits. If any value is outside its limit, the result is **Not Potable**, and the reasons are listed.
4. **Step 2, machine learning:** if all values are within the limits, a trained Random Forest model predicts Potable or Not Potable and shows its confidence.
5. The website displays the result and a short reminder that laboratory testing is needed.

## Tech stack
- **Model:** Python, pandas, scikit-learn (Random Forest)
- **Backend:** FastAPI + Uvicorn
- **Frontend:** HTML, CSS, JavaScript (dark water-themed interface)
- **Version control:** Git and GitHub

## Project structure
```
water-potability-predictor/
├── data/
│   └── water_potability.csv
├── model/
│   ├── train.py
│   ├── compare.py
│   └── model.joblib
├── backend/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt
└── README.md
```

## Input parameters
| Parameter | Unit |
|---|---|
| pH | 0 to 14 |
| Hardness | mg/L |
| Solids (TDS) | ppm |
| Chloramines | ppm |
| Sulfate | mg/L |
| Conductivity | µS/cm |
| Organic carbon | ppm |
| Trihalomethanes | µg/L |
| Turbidity | NTU |

## Safety rules (checked before the model)
A sample is marked **Not Potable** if any of the following is true:

| Parameter | Not Potable if |
|---|---|
| pH | below 6.5 or above 8.5 |
| Hardness | above 600 mg/L |
| Solids (TDS) | above 2000 ppm |
| Chloramines | above 4 ppm |
| Sulfate | above 400 mg/L |
| Trihalomethanes | above 80 µg/L |
| Turbidity | above 5 NTU |

Conductivity and organic carbon have no single clear limit, so they are used only by the model. The limits are based on commonly used drinking-water guidelines (WHO and BIS IS 10500) and should be checked against the latest official documents.

## Run locally
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python model/train.py
uvicorn backend.main:app --reload
```
Then open http://127.0.0.1:8000 in a browser.

## Model results
- **Dataset:** public Kaggle "Water Potability" dataset (3,276 samples, 9 parameters)
- **Model:** Random Forest (300 trees, class-balanced), missing values filled with the median
- **Test accuracy:** 64.9% (656 test samples, 80/20 split)
- **Majority-class baseline:** 61% (always predicting "Not Potable")

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Not Potable | 0.68 | 0.80 | 0.74 |
| Potable | 0.57 | 0.42 | 0.48 |

### Model comparison (5-fold cross-validation accuracy)
| Features | Logistic Regression | Random Forest | Gradient Boosting |
|---|---|---|---|
| 4 (pH, Hardness, Solids, Turbidity) | 0.510 | 0.575 | 0.607 |
| All 9 | 0.505 | 0.668 | 0.657 |

With only four parameters, no model clearly beat the 61% baseline, so the final model uses all nine. The dataset's labels do not always follow health standards (some samples with very poor values are labelled potable), which limits accuracy. This is why the rule-based safety check runs before the model.

## Limitations
- The dataset is not from Warangal, so results cannot be assumed to apply to local water sources.
- The dataset is small and noisy, so model accuracy is moderate (about 65%).
- About 43% of the model's "Potable" predictions are incorrect, so a "Potable" result must never be treated as proof of safety.
- Real water safety also depends on bacteria, heavy metals and other chemicals that are not measured here.

## Future work
- Collect lab-verified water samples from Warangal sources and retrain the model.
- Validate the model locally before any real-world use.
- Allow optional fields so users can get a prediction with fewer measurements.
- Explore better models and additional parameters.

## Author
-Macherla Prajwala Sai
Team Mates:1.Motla Roja
           2.Arelly Mugdha
           3.Sanith Kumar
           4.D.Sreethu
