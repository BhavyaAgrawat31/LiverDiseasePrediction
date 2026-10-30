
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Liver Disease Prediction API")

# Project folders
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "liver_model.pkl"

# Features must match the order and names used during training
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
]

# Load the already-trained model
model = None
model_error = None

try:
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    model_error = str(exc)


class PatientInput(BaseModel):
    Age: int = Field(ge=1, le=120)
    Gender: str
    Total_Bilirubin: float = Field(ge=0)
    Direct_Bilirubin: float = Field(ge=0)
    Alkaline_Phosphotase: float = Field(ge=0)
    Alamine_Aminotransferase: float = Field(ge=0)
    Aspartate_Aminotransferase: float = Field(ge=0)
    Total_Protiens: float = Field(ge=0)
    Albumin: float = Field(ge=0)
    Albumin_and_Globulin_Ratio: float = Field(ge=0)


@app.get("/")
def home():
    return {
        "message": "Liver Disease Prediction API is running",
        "model_loaded": model is not None,
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_error": model_error,
    }


@app.post("/predict")
def predict(patient: PatientInput):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail=f"Model is not loaded. Check models/liver_model.pkl. Error: {model_error}",
        )

    try:
        patient_data = patient.model_dump()
        patient_data["Gender"] = patient_data["Gender"].strip().capitalize()

        if patient_data["Gender"] not in ["Male", "Female"]:
            raise HTTPException(
                status_code=422,
                detail="Gender must be Male or Female.",
            )

        # Preserve the feature names and order used during training
        input_df = pd.DataFrame(
            [[patient_data[name] for name in FEATURES]],
            columns=FEATURES,
        )
        input_df = pd.DataFrame(
    [[patient_data[name] for name in FEATURES]],
    columns=FEATURES,
)

        input_df["AST_ALT_Ratio"] = (
            input_df["Aspartate_Aminotransferase"]
            / input_df["Alamine_Aminotransferase"].replace(0, 1e-6)
        )

        prediction = int(model.predict(input_df)[0])

        result = {
            "prediction": prediction,
            "label": (
                "Liver Disease Class"
                if prediction == 1
                else "Non-Liver Disease Class"
            ),
            "message": (
                "The model predicts the liver-patient class."
                if prediction == 1
                else "The model predicts the non-liver-patient class."
            ),
        }

        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            classes = list(model.classes_)

            if 1 in classes:
                result["probability"] = float(
                    probabilities[classes.index(1)]
                )

        return result

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(exc)}",
        )
