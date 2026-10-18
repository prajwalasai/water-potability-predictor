import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# The 4 inputs the website will ask for
FEATURES = ["ph", "Hardness", "Solids", "Turbidity"]

# 1. Load data
df = pd.read_csv("data/water_potability.csv")
X = df[FEATURES]
y = df["Potability"]

# 2. Split into training and testing parts
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Build the model (the imputer fills missing values)
model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("rf", RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42,
    )),
])

# 4. Train
model.fit(X_train, y_train)

# 5. Test and print results
pred = model.predict(X_test)
print("Accuracy:", round(accuracy_score(y_test, pred), 3))
print(classification_report(y_test, pred, target_names=["Not Potable", "Potable"]))

# 6. Save the trained model
joblib.dump(model, "model/model.joblib")
print("Model saved to model/model.joblib")