import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from core.database import Base, get_db
from models.user import User

# Use a clean, separate in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_fraud.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    """Initializes a clean schema and seeds basic testing accounts."""
    Base.metadata.create_all(bind=engine)
    # Seed default user and admin for test scoping
    db = TestingSessionLocal()
    from core.security import get_password_hash
    db.add(User(username="test_admin", email="t_admin@test.com", hashed_password=get_password_hash("testpwd"), role="admin"))
    db.add(User(username="test_user", email="t_user@test.com", hashed_password=get_password_hash("testpwd"), role="user"))
    db.commit()
    db.close()
    yield
    # Dispose of engine to release open file locks on Windows
    engine.dispose()
    if os.path.exists("./test_fraud.db"):
        try:
            os.remove("./test_fraud.db")
        except Exception:
            pass

@pytest.fixture(scope="function")
def db_session():
    """Yields a database session and rollbacks changes at the end."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client():
    """FastAPI TestClient overriding database session dependency."""
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="module")
def user_auth_headers(client):
    """Logs in test_user and yields bearer auth headers."""
    response = client.post("/api/auth/login", json={"username": "test_user", "password": "testpwd"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="module")
def admin_auth_headers(client):
    """Logs in test_admin and yields bearer auth headers."""
    response = client.post("/api/auth/login", json={"username": "test_admin", "password": "testpwd"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- TESTS ---

def test_auth_register_and_login(client):
    # 1. Register new user
    reg_payload = {"username": "new_guy", "email": "newguy@mail.com", "password": "securepassword"}
    response = client.post("/api/auth/register", json=reg_payload)
    assert response.status_code == 201
    assert response.json()["username"] == "new_guy"
    assert "id" in response.json()
    
    # 2. Login
    login_payload = {"username": "new_guy", "password": "securepassword"}
    response = client.post("/api/auth/login", json=login_payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["role"] == "user"

def test_unauthorized_endpoints(client):
    # Try fetching history without JWT
    response = client.get("/api/transactions/history")
    assert response.status_code == 401

def test_predict_and_metrics(client, user_auth_headers):
    # Submit standard transaction for prediction
    payload = {
        "card_number": "1234567812345678",
        "amount": 250.00,
        "merchant": "Apple Store",
        "profile": "genuine"
    }
    response = client.post("/api/transactions/predict", json=payload, headers=user_auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 250.00
    assert data["merchant"] == "Apple Store"
    assert data["status"] in ["APPROVED", "REVIEW", "BLOCKED"]
    assert "prediction" in data
    assert data["prediction"]["probability"] >= 0.0
    
    # Fetch metrics
    metrics_res = client.get("/api/transactions/metrics", headers=user_auth_headers)
    assert metrics_res.status_code == 200
    metrics = metrics_res.json()
    assert metrics["total_count"] >= 1
    assert metrics["total_amount"] >= 250.00

def test_role_based_history(client, user_auth_headers, admin_auth_headers):
    # User submits a transaction
    client.post(
        "/api/transactions/predict",
        json={"card_number": "1111222233334444", "amount": 10.0, "merchant": "Target", "profile": "genuine"},
        headers=user_auth_headers
    )
    
    # Admin submits a transaction
    client.post(
        "/api/transactions/predict",
        json={"card_number": "5555666677778888", "amount": 99.99, "merchant": "BestBuy", "profile": "genuine"},
        headers=admin_auth_headers
    )
    
    # User gets history -> Should see user's transactions only
    user_res = client.get("/api/transactions/history", headers=user_auth_headers)
    user_txs = user_res.json()
    
    # Admin gets history -> Should see all transactions
    admin_res = client.get("/api/transactions/history", headers=admin_auth_headers)
    admin_txs = admin_res.json()
    
    assert len(admin_txs) > len(user_txs)

def test_admin_override(client, user_auth_headers, admin_auth_headers):
    # 1. Create a transaction that is flagged for REVIEW/BLOCK using fraud profile
    tx_res = client.post(
        "/api/transactions/predict",
        json={"card_number": "9999999999999999", "amount": 1200.0, "merchant": "Jewelry Shop", "profile": "fraudulent"},
        headers=user_auth_headers
    )
    tx_data = tx_res.json()
    tx_id = tx_data["id"]
    assert tx_data["status"] == "BLOCKED"
    
    # 2. Try overriding as user -> should fail (403 Forbidden)
    user_override = client.patch(
        f"/api/transactions/transactions/{tx_id}/override?target_status=APPROVED", # note prefix is /api/transactions
        headers=user_auth_headers
    )
    # Correct url route path check: it's /api/transactions/{id}/override
    user_override = client.patch(
        f"/api/transactions/{tx_id}/override?target_status=APPROVED",
        headers=user_auth_headers
    )
    assert user_override.status_code == 403
    
    # 3. Override as admin -> should succeed
    admin_override = client.patch(
        f"/api/transactions/{tx_id}/override?target_status=APPROVED",
        headers=admin_auth_headers
    )
    assert admin_override.status_code == 200
    assert admin_override.json()["status"] == "APPROVED"
