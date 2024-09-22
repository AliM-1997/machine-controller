import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_success():
    response = client.post("/api/v1/predict", json={
        "air_temperature": 320.0,
        "process_temperature": 340.0,
        "rotational_speed": 3000,
        "torque": 150,
        "tool_wear": 9000,
        "machine_lifetime": 1000,
        "lifecycle": 80,
        "operational_time": 1500
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert "probabilities" in data

def test_predict_missing_fields():
    response = client.post("/api/v1/predict", json={
        "air_temperature": 320.0,
        "process_temperature": 340.0,
        "rotational_speed": 3000,
        "torque": 150,
        "tool_wear": 1200,
        "machine_lifetime": 1000
        # Missing lifecycle and operational_time
    })

    assert response.status_code == 422
    assert "detail" in response.json()
    assert any(field["loc"] == ["body", "lifecycle"] for field in response.json()["detail"])
    assert any(field["loc"] == ["body", "operational_time"] for field in response.json()["detail"])

def test_predict_invalid_data_type():
    response = client.post("/api/v1/predict", json={
        "air_temperature": "invalid",  # Invalid data type
        "process_temperature": 340.0,
        "rotational_speed": 3000,
        "torque": 150,
        "tool_wear": 1200,
        "machine_lifetime": 1000,
        "lifecycle": 80,
        "operational_time": 1500
    })

    assert response.status_code == 422
    assert "detail" in response.json()
    assert any(field["loc"] == ["body", "air_temperature"] for field in response.json()["detail"])
