from urllib import response
from jose import jwt
from app import schemas
from app.config import settings
import pytest

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from docker environment"}



def test_create_user(client):
    response = client.post("/users/", json=
	{
	"email": "kaley12.smith@gmail.com",
	"password":"kal123"
	})
    new_user =  schemas.UserOut(**response.json())
    assert new_user.email == "kaley12.smith@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post("login", data={
	"username": test_user["email"],
	"password": test_user["password"]
	})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200




@pytest.mark.parametrize("email, password, status_code",
[
    ("wrongemailAndOr", "wrongPassword", 403),
    (None, "somePassword", 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post("/login", data={
        "username": email,
        "password": password
    })
    #assert response.json().get("detail") == "Invalid Credentials"
