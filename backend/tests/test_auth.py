def test_register_new_user(client):
    response = client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "TestPass123",
        "full_name": "Test User",
        "role": "patient",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_register_duplicate_email_fails(client):
    payload = {
        "email": "dup@example.com",
        "password": "TestPass123",
        "full_name": "Dup User",
        "role": "patient",
    }
    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "loginuser@example.com",
        "password": "TestPass123",
        "full_name": "Login User",
        "role": "patient",
    })
    response = client.post("/auth/login", json={
        "email": "loginuser@example.com",
        "password": "TestPass123",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password_fails(client):
    client.post("/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "CorrectPass123",
        "full_name": "Wrong Pass User",
        "role": "patient",
    })
    response = client.post("/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "IncorrectPass",
    })
    assert response.status_code == 401