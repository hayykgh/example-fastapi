from app import schemas
import pytest


# def test_root(client):
#     res = client.get('/')
#     assert res.json().get('message') == "a new message"
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hayykgh3@gmail.com", "password": "Samura1!"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hayykgh3@gmail.com"
    assert res.status_code == 201



def test_login_user(client, test_user):
    res =client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())


    assert login_res.token_type == "bearer"
    assert res.status_code == 200 


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("ha1kgh@gmail.com", "WrongPassword", 403),
        ("WrongEmail@gmail.com", "WrongPassword", 403),
        ("ha1kgh@gmail.com", None, 422),
        (None, "Samura1!", 422)
    ]
)
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password}
    )
    
    assert res.status_code == status_code