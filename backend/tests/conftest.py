import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.db.models import Task
import os
from contextlib import contextmanager

@contextmanager
def temp_database():
    """
    Context manager para criar e limpar banco temporário.
    """
    test_db_path = "test_database.db"
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{test_db_path}"
    
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    
    try:
        yield db, engine
    finally:
        db.close()
        engine.dispose()
        
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture usando context manager.
    """
    with temp_database() as (db, engine):
        yield db

@pytest.fixture(name="client")
def client_fixture(db_session: Session):
    """
    Fixture mais robusta para TestClient com override de dependência.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    original_overrides = app.dependency_overrides.copy()
    
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        client = TestClient(app)
        yield client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)

@pytest.fixture(name="test_user_credentials")
def test_user_credentials_fixture():
    """
    Provides standard credentials for a test user.
    These credentials are used by other authentication fixtures.
    """
    return {"username": "user", "password": "password"}

@pytest.fixture(name="auth_token")
def auth_token_fixture(client: TestClient, test_user_credentials: dict):
    """
    Performs a login with the test user and returns the access token.
    'create_test_user' ensures the user is already in the database.
    """
    response = client.post(
        "/api/v1/login",
        data={
            "username": test_user_credentials["username"],
            "password": test_user_credentials["password"]
        }
    )
    assert response.status_code == 200, f"Login failed for auth_token fixture: {response.json()}"
    
    token_data = response.json()
    assert "access_token" in token_data
    return token_data["access_token"]