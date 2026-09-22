def register_and_login(client, email, role="patient"):
    """Registers a *patient* (role is not settable via the public endpoint
    any more) and logs in. For doctor/admin accounts, use create_staff_and_login."""
    client.post("/auth/register", json={
        "email": email, "password": "TestPass123", "full_name": "Test",
    })
    login_response = client.post("/auth/login", json={"email": email, "password": "TestPass123"})
    return login_response.json()["access_token"]


def create_staff_and_login(client, admin_token, email, role):
    client.post(
        "/admin/users",
        json={"email": email, "password": "TestPass123", "full_name": "Test", "role": role},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    login_response = client.post("/auth/login", json={"email": email, "password": "TestPass123"})
    return login_response.json()["access_token"]


def test_patient_cannot_access_doctor_endpoint(client):
    token = register_and_login(client, "patientrbac@example.com")
    response = client.get("/doctor/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_doctor_can_access_doctor_endpoint(client, admin_token):
    token = create_staff_and_login(client, admin_token, "doctorrbac@example.com", "doctor")
    response = client.get("/doctor/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_doctor_cannot_access_admin_endpoint(client, admin_token):
    token = create_staff_and_login(client, admin_token, "doctornotadmin@example.com", "doctor")
    response = client.get("/admin/stats", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_cannot_self_register_as_doctor_or_admin(client):
    """Regression test: role must not be settable via public registration."""
    response = client.post("/auth/register", json={
        "email": "wannabe-admin@example.com", "password": "TestPass123",
        "full_name": "Test", "role": "admin",
    })
    assert response.status_code == 200  # registration itself still succeeds...
    token = response.json()["access_token"]

    # ...but the resulting account must be a plain patient, not an admin.
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["role"] == "patient"

    admin_check = client.get("/admin/stats", headers={"Authorization": f"Bearer {token}"})
    assert admin_check.status_code == 403


def test_non_admin_cannot_create_staff(client):
    token = register_and_login(client, "notanadmin@example.com")
    response = client.post(
        "/admin/users",
        json={"email": "sneaky@example.com", "password": "TestPass123", "full_name": "Test", "role": "admin"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403