import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv("data/water_potability.csv")
y = df["Potability"]

FOUR = ["ph", "Hardness", "Solids", "Turbidity"]
ALL = [c for c in df.columns if c != "Potability"]

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
print("Majority-class baseline:", round(1 - y.mean(), 3))

for fname, feats in [("4 features", FOUR), ("All 9 features", ALL)]:
    for mname, m in models.items():
        pipe = Pipeline([
            ("imp", SimpleImputer(strategy="median")),
            ("sc", StandardScaler()),
            ("m", m),
        ])
        score = cross_val_score(pipe, df[feats], y, cv=cv, scoring="accuracy").mean()
        print(f"{fname:15} | {mname:20} | accuracy {score:.3f}")