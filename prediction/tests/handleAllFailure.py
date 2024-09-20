import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.predictions import predict
from app.schemas import MachineData

test_cases = [
    MachineData(
        air_temperature=320.0,
        process_temperature=340.0,
        rotational_speed=7000,
        torque=150,
        tool_wear=1200,
        lifecycle=75,
        operational_time=5000
    ),
    MachineData(
        air_temperature=320.0,
        process_temperature=340.0,
        rotational_speed=3000,
        torque=150,
        tool_wear=1200,
        lifecycle=10,  
        operational_time=100
    ),
]

results = []

for case in test_cases:
    result = predict(case)
    results.append({
        "input": case.dict(),  
        "prediction": result["predictions"],
        "probabilities": result["probabilities"]
    })

with open('test_results.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Test results saved to 'test_results.json'.")
