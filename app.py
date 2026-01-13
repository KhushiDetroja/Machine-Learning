from flask import Flask, render_template, request
import numpy as np
import joblib

#app = Flask(__name__)
app = Flask(__name__, template_folder='frontend/templates')

# ===============================
# Load ML artifacts
# ===============================
model = joblib.load("random_forest_model.pkl")
scaler = joblib.load("scaler.pkl")

# IMPORTANT: feature order used during training
FEATURE_ORDER = [
    "age",
    "gender",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active"
]

# ===============================
# Page Routes
# ===============================
@app.route('/')
def base():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/visuals')
def visuals():
    return render_template('visuals.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/model')
def model_info():
    return render_template('model.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

# ===============================
# Prediction Page (GET)
# ===============================
@app.route('/predict', methods=['GET'])
def predict_page():
    return render_template('predict.html')

# ===============================
# Prediction Logic (POST)
# ===============================
@app.route('/predict-result', methods=['POST'])
def predict_result():
    try:
        # Collect form inputs (EXACT ORDER)
        input_values = [
            float(request.form['age']),
            int(request.form['gender']),
            float(request.form['height']),
            float(request.form['weight']),
            float(request.form['ap_hi']),
            float(request.form['ap_lo']),
            int(request.form['cholesterol']),
            int(request.form['gluc']),
            int(request.form['smoke']),
            int(request.form['alco']),
            int(request.form['active'])
        ]
    
        # Convert to numpy array
        input_data = np.array([input_values])
    
        # Scale input using TRAINED scaler
        input_scaled = scaler.transform(input_data)
    
        # Model prediction
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1] * 100
    
        # Result message
        risk_level = "High" if prediction == 1 else "Low"
        result = f"{risk_level} risk of cardiovascular disease ({probability:.2%})"

        # Logic for customized messaging
        if probability < 30:
            status = "Optimal"
            message = "Your cardiovascular profile looks strong. Maintain your current lifestyle."
            advice = "Continue regular exercise and a balanced diet. Annual check-ups are recommended."
            color = "success"
        elif 30 <= probability < 70:
            status = "Borderline / Elevated"
            message = "Some markers indicate an emerging risk. Precautionary changes are advised."
            advice = "Monitor your blood pressure weekly and reduce sodium intake. Consult a physician."
            color = "warning"
        else:
            status = "High Risk"
            message = "Multiple clinical indicators suggest a high probability of heart disease."
            advice = "Please schedule a consultation with a cardiologist immediately for a full evaluation."
            color = "danger"

        return render_template('predict.html', 
                               prediction_text=result, 
                               probability=probability,
                               risk=probability, 
                               status=status, 
                               message=message, 
                               advice=advice, 
                               color=color)
    except Exception as e:
        return render_template('predict.html', prediction_text=f"Error processing input: {str(e)}")

# ===============================
# Run App
# ===============================
if __name__ == "__main__":
    app.run(debug=True, port=5001)

