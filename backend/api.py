from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import joblib
import pandas as pd
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Load all saved components ---
model = joblib.load("LatencyPredictionModel/xgb_regression_model.pkl")
scaler = joblib.load("LatencyPredictionModel/scaler.pkl")
label_encoders = joblib.load("LatencyPredictionModel/label_encoder.pkl")

# Load expected feature names (used in training)
features = joblib.load("LatencyPredictionModel/features_list.pkl")

@app.route('/predict', methods=['POST'])
def predict_delay():
    try:
        # --- Get input data from the request ---
        user_input = request.json

        # --- Convert to DataFrame ---
        input_df = pd.DataFrame([user_input])

        # --- Handle Categorical Encoding with Error Handling ---
        for col in ["Train ID", "Station Name"]:
            le = label_encoders[col]
            if user_input[col] not in le.classes_:
                return jsonify({"error": f"'{user_input[col]}' not seen during training for {col}. Available classes: {list(le.classes_)}"}), 400
            input_df[col] = le.transform([user_input[col]])

        # --- Feature Engineering: Convert Date & Time ---
        input_df["Date"] = pd.to_datetime(input_df["Date"])
        input_df["Weekday"] = input_df["Date"].dt.weekday 

        # Convert "HH:MM" to hour & minute
        arrival_time = datetime.strptime(user_input["Arrival Time"], "%H:%M")
        input_df["Arrival_Hour"] = arrival_time.hour
        input_df["Arrival_Minute"] = arrival_time.minute

        # Example Features (make sure these exist in your model)
        input_df["Planned_Hour"] = input_df["Arrival_Hour"]
        input_df["Planned_Minute"] = input_df["Arrival_Minute"]  
        input_df["Actual_Hour"] = input_df["Arrival_Hour"]  
        input_df["Actual_Minute"] = input_df["Arrival_Minute"]  
        input_df["Train_Station_Avg_Delay"] = 0  
        input_df["Station_Peak_Delay"] = 0  
        input_df["Train_Avg_Delay"] = 0 

        # Drop unused raw columns
        input_df = input_df.drop(["Date", "Arrival Time"], axis=1)

        # --- Ensure All Features Are Present ---
        for feature in features:
            if feature not in input_df.columns:
                input_df[feature] = 0  # Add missing features as 0 or appropriate value

        # --- Reorder columns to match training order ---
        input_df = input_df[features]

        # --- Apply Scaling ---
        X_scaled = scaler.transform(input_df)

        # --- Predict Delay ---
        predicted_delay_mins = model.predict(X_scaled)[0]

        # --- Calculate Predicted Arrival Time ---
        predicted_arrival_time = arrival_time + timedelta(minutes=float(predicted_delay_mins))

        # --- Output ---
        response = {
            "Predicted Delay": round(predicted_delay_mins, 2),
            "Scheduled Arrival": arrival_time.strftime('%H:%M'),
            "Predicted Arrival Time": predicted_arrival_time.strftime('%H:%M')
        }

        # --- Return the response ---
        return jsonify({
    #"predicted_delay_minutes": float(round(predicted_delay_mins, 2)),  # Cast to Python float
    #"scheduled_arrival": arrival_time.strftime('%H:%M'),
    "predicted_arrival_time": predicted_arrival_time.strftime('%H:%M')
})


    except Exception as e:
        return jsonify({"error": str(e)}), 500

JSON_FILE = 'src/data/mainlinealerts.json'

def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)


# API to get all alerts
@app.route('/alerts', methods=['GET'])
def get_alerts():
    try:
        data = load_data()
        return jsonify(data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to add a new alert
@app.route('/alerts', methods=['POST'])
def add_alert():
    try:
        new_alert = request.json
        data = load_data()

        # Automatically assign next ID
        new_alert['id'] = max([item['id'] for item in data], default=0) + 1

        ordered_alert = {
            "id": new_alert["id"],
            "message": new_alert["message"],
            "time": new_alert["time"]
        }

        data.append(ordered_alert)
        save_data(data)
        return jsonify({"message": "Alert added successfully", "data": ordered_alert}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
