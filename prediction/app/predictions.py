import pandas as pd
import joblib
import os
from fastapi import HTTPException

model_path = 'model/model.pkl'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

model = joblib.load(model_path)
required_columns = model.feature_names_in_.tolist()

def predict(data):
    try:
        input_data_dict = {
            'Air Temperature (K)': data.air_temperature,
            'Process Temperature (K)': data.process_temperature,
            'Rotational Speed (RPM)': data.rotational_speed,
            'Torque (Nm)': data.torque,
            'Tool Wear (hours)': data.tool_wear,
            'Lifecycle (%)': data.lifecycle,
            'Operational Time (hours)': data.operational_time
        }

        input_data = pd.DataFrame([input_data_dict])

        for col in required_columns:
            if col not in input_data.columns:
                input_data[col] = 0
        
        input_data = input_data[required_columns]

        predictions = model.predict(input_data)
        predictions_proba = model.predict_proba(input_data)

        failure_types = {
            0: 'No_Failure',
            1: 'Heat_Dissipation_Failure',
            2: 'Overstrain_Failure',
            3: 'Power_Failure',
            4: 'Tool_Wear_Failure'
        }


        translated_predictions = [failure_types[int(pred)] for pred in predictions]

        probabilities = [
            {failure_types[i]: float(prob) for i, prob in enumerate(probs)}
            for probs in predictions_proba
        ]

        response = {
            "predictions": translated_predictions,
            "probabilities": probabilities
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
