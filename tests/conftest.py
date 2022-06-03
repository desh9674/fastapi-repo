from urllib import response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from app import models
from app.database import get_db, Base
from app.oauth2 import create_access_token
import pytest
#pytest -v -s tests\test_users.py
#pytest -v -s tests\test_users.py -x "x" flag stops after first fail test

#client = TestClient(app)
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:desh1596@localhost:5432/test_fastapi'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL  #, connect_args={"check_same_thread": False} #only for sqlite
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base() #

# Dependency


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # run our code after our test finishes

@pytest.fixture
def test_user2(client):
    user_data = {
        "email":"test.user2@gmail.com",
        "password": "pass1234"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
   
    new_user =  response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user(client):
    user_data = {
        "email":"test.user@gmail.com",
        "password": "pass"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
   
    new_user =  response.json()
    new_user["password"] = user_data["password"]
    return new_user




@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization":f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {
            "title": "first title",
            "content" : "first content",
            "owner_id" : test_user["id"]
        },
        {
            "title": "2nd title",
            "content" : "2nd content",
            "owner_id" : test_user["id"]
        },
        {
            "title": "user2 Title",
            "content" : "user2 content",
            "owner_id" : test_user2["id"]
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    posts = list(map(create_post_model, post_data))
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts