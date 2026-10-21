import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
)
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

FEATURES = [
    "ph", "Hardness", "Solids", "Chloramines", "Sulfate",
    "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity",
]

df = pd.read_csv("data/water_potability.csv")
X = df[FEATURES]
y = df["Potability"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

candidates = {
    "Random Forest": (
        Pipeline([
            ("imp", SimpleImputer(strategy="median")),
            ("m", RandomForestClassifier(random_state=42, n_jobs=-1)),
        ]),
        {
            "m__n_estimators": [300, 500, 800],
            "m__max_depth": [None, 10, 20, 30],
            "m__min_samples_leaf": [1, 2, 3, 5],
            "m__max_features": ["sqrt", "log2", 0.5],
        },
    ),
    "Extra Trees": (
        Pipeline([
            ("imp", SimpleImputer(strategy="median")),
            ("m", ExtraTreesClassifier(random_state=42, n_jobs=-1)),
        ]),
        {
            "m__n_estimators": [300, 500, 800],
            "m__max_depth": [None, 10, 20, 30],
            "m__min_samples_leaf": [1, 2, 3, 5],
            "m__max_features": ["sqrt", "log2", 0.5],
        },
    ),
    "Hist Gradient Boosting": (
        HistGradientBoostingClassifier(random_state=42),
        {
            "learning_rate": [0.01, 0.03, 0.05, 0.1],
            "max_depth": [None, 3, 5, 8],
            "max_iter": [100, 200, 400],
            "min_samples_leaf": [10, 20, 40],
            "l2_regularization": [0, 0.1, 1.0],
        },
    ),
}

best_name, best_search = None, None

for name, (estimator, grid) in candidates.items():
    print(f"Tuning {name} ...")
    search = RandomizedSearchCV(
        estimator, grid, n_iter=20, cv=cv,
        scoring="accuracy", random_state=42, n_jobs=-1,
    )
    search.fit(X_train, y_train)
    print(f"  best CV accuracy: {search.best_score_:.3f}")
    if best_search is None or search.best_score_ > best_search.best_score_:
        best_name, best_search = name, search

print("\nBest model:", best_name)
print("Best settings:", best_search.best_params_)

model = best_search.best_estimator_
pred = model.predict(X_test)
print("\nTest accuracy:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred, target_names=["Not Potable", "Potable"]))

joblib.dump(model, "model/model.joblib")
print("Model saved to model/model.joblib")