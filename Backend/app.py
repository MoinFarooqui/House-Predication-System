#app.py

from flask import Flask, render_template, request
import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "..", "Frontend"),
    static_folder=os.path.join(BASE_DIR, "..", "Frontend")
)

# Load model and scaler
model = joblib.load(os.path.join(BASE_DIR, "model.joblib"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.joblib"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    GrLivArea = float(request.form["GrLivArea"])
    OverallQual = int(request.form["OverallQual"])
    YearBuilt = int(request.form["YearBuilt"])
    TotalBsmtSF = float(request.form["TotalBsmtSF"])
    FullBath = int(request.form["FullBath"])
    TotRmsAbvGrd = int(request.form["TotRmsAbvGrd"])

    features = np.array([[GrLivArea, OverallQual, YearBuilt,
                          TotalBsmtSF, FullBath, TotRmsAbvGrd]])

    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)[0]

    return render_template(
        "index.html",
        prediction_text=f"Predicted House Price: ${prediction:,.2f}"
    )

if __name__ == "__main__":
    app.run(debug=True)