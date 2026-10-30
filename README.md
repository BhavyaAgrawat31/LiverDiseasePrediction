# Liver Disease Prediction Using Machine Learning

## Project Overview
This project uses Machine Learning techniques to predict the possibility of liver disease based on patient medical attributes.

A Random Forest classifier is used for prediction, and the trained model is integrated into a web application using Streamlit and FastAPI.

## Dataset
- Dataset: Indian Liver Patient Dataset (ILPD)
- 583 records
- 10 input features
- Target variable: Dataset

## Technologies Used
- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- Streamlit
- FastAPI
- Joblib

## Machine Learning Models
1. Logistic Regression
2. Random Forest Classifier

Random Forest was selected for the final prediction application.

## Application
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Model:** Trained Random Forest classifier

Users can enter patient details through the web interface and receive a prediction.

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn main:app --reload
```

Run the frontend in another terminal:

```bash
streamlit run app.py
```

## Disclaimer
This project is developed for educational purposes only. Its predictions should not be considered a medical diagnosis.
