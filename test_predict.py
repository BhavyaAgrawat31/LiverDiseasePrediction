
from predict import predict_liver_disease

sample_patient = {
    "Age": 45,
    "Gender": "Male",
    "Total_Bilirubin": 1.2,
    "Direct_Bilirubin": 0.3,
    "Alkaline_Phosphotase": 200,
    "Alamine_Aminotransferase": 30,
    "Aspartate_Aminotransferase": 35,
    "Total_Protiens": 6.8,
    "Albumin": 3.5,
    "Albumin_and_Globulin_Ratio": 1.0,
}

result = predict_liver_disease(sample_patient)

print("Prediction result:")
print(result)
