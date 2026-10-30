
import joblib
import pandas as pd
from pathlib import Path

# Locate and load the trained model
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "liver_model.pkl"

model = joblib.load(MODEL_PATH)

# Exact features used during training
FEATURES = [
    "Age",
    "Gender",
    "Total_Bilirubin",
    "Direct_Bilirubin",
    "Alkaline_Phosphotase",
    "Alamine_Aminotransferase",
    "Aspartate_Aminotransferase",
    "Total_Protiens",
    "Albumin",
    "Albumin_and_Globulin_Ratio",
    "AST_ALT_Ratio",
]


def predict_liver_disease(patient_data):
    """Return a prediction from the saved ML pipeline."""

    # Calculate the engineered feature
    patient_data = patient_data.copy()

    alt = patient_data["Alamine_Aminotransferase"]
    ast = patient_data["Aspartate_Aminotransferase"]

    patient_data["AST_ALT_Ratio"] = ast / alt if alt != 0 else 0

    # Keep feature names and order consistent with training
    input_df = pd.DataFrame(
        [[patient_data[feature] for feature in FEATURES]],
        columns=FEATURES,
    )

    prediction = int(model.predict(input_df)[0])

    result = {
        "prediction": prediction,
        "message": (
            "Possible liver disease detected by the model"
            if prediction == 1
            else "The model did not predict liver disease"
        ),
    }

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        result["probabilities"] = {
            str(label): float(probability)
            for label, probability in zip(
                model.classes_, probabilities
            )
        }

    return result
