# app.py
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model and scaler
model = joblib.load("model.joblib")
scaler = joblib.load("scaler.joblib")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Get form data
    GrLivArea = float(request.form["GrLivArea"])
    OverallQual = int(request.form["OverallQual"])
    YearBuilt = int(request.form["YearBuilt"])
    TotalBsmtSF = float(request.form["TotalBsmtSF"])
    FullBath = int(request.form["FullBath"])
    TotRmsAbvGrd = int(request.form["TotRmsAbvGrd"])

    # Prepare input
    features = np.array([[GrLivArea, OverallQual, YearBuilt, TotalBsmtSF, FullBath, TotRmsAbvGrd]])
    features_scaled = scaler.transform(features)

    # Predict
    prediction = model.predict(features_scaled)[0]

    return render_template("index.html", prediction_text=f"Predicted House Price: ${prediction:,.2f}")

if __name__ == "__main__":
    app.run(debug=True)