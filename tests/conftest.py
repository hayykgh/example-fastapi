from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.oauth2 import create_access_token
from app.database import get_db


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "ha1kgh@gmail.com",
        "password": "Samura1!",
        "first_name": "Hayk",
        "last_name": "Ghazaryan",
    }


    res = client.post("/users", json=user_data)
    new_user = res.json()
    new_user["password"]=user_data["password"]

    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"], "first_name": test_user["first_name"], "last_name": test_user["last_name"],  "user_email": test_user["email"] })

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client



@pytest.fixture
def test_post(authorized_client, test_user):

    posts = []
    for i in range(4):
        post_data = {
            "title": f"Title {i}",
            "content": f"Content number {i}",
            "owner_id": test_user['id']
        }
        res = authorized_client.post("/posts", json=post_data)
        posts.append(res.json())
    return posts
