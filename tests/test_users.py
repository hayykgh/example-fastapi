from app import schemas   


def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == "a new message"
    assert res.status_code == 200


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

