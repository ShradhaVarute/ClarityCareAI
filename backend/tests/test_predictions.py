def test_heart_disease_prediction(client):
    client.post("/auth/register", json={
        "email": "predictpatient@example.com",
        "password": "TestPass123",
        "full_name": "Predict Patient",
        "role": "patient",
    })
    login_response = client.post("/auth/login", json={
        "email": "predictpatient@example.com",
        "password": "TestPass123",
    })
    token = login_response.json()["access_token"]

    response = client.post(
        "/predictions/heart_disease",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "patient_id": 1,
            "features": {
                "age": 55, "sex": 1, "cp": 3, "trestbps": 130, "chol": 250,
                "fbs": 0, "restecg": 0, "thalach": 150, "exang": 0,
                "oldpeak": 1.5, "slope": 1, "ca": 0, "thal": 2,
            },
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "explanation" in data
    assert len(data["explanation"]) > 0