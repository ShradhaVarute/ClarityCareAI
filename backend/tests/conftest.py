import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ.setdefault(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/claritycare_test_db"
)

from app.main import app
from app.core.database import Base, get_db

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def _reset_rate_limits():
    from app.routes.auth import limiter
    limiter.reset()
    yield


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_token(client, db_session):
    """Bootstraps an admin the way scripts/create_admin.py does in real
    deployments (direct DB insert), then logs in through the real API.
    Doctor/admin accounts can't be self-registered, so tests that need one
    start from here rather than POST /auth/register."""
    from app.core.security import hash_password
    from app.models.user import User

    admin = User(
        email="bootstrap-admin@example.com",
        hashed_password=hash_password("AdminPass123"),
        role="admin",
    )
    db_session.add(admin)
    db_session.commit()

    response = client.post("/auth/login", json={
        "email": "bootstrap-admin@example.com",
        "password": "AdminPass123",
    })
    return response.json()["access_token"]