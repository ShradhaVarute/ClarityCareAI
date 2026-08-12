def register_and_login(client, email, role):
    client.post("/auth/register", json={
        "email": email, "password": "TestPass123",
        "full_name": "Test", "role": role,
    })
    login_response = client.post("/auth/login", json={"email": email, "password": "TestPass123"})
    return login_response.json()["access_token"]


def test_patient_cannot_access_doctor_endpoint(client):
    token = register_and_login(client, "patientrbac@example.com", "patient")
    response = client.get("/doctor/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_doctor_can_access_doctor_endpoint(client):
    token = register_and_login(client, "doctorrbac@example.com", "doctor")
    response = client.get("/doctor/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_doctor_cannot_access_admin_endpoint(client):
    token = register_and_login(client, "doctornotadmin@example.com", "doctor")
    response = client.get("/admin/stats", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403