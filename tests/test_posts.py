def test_getting_all_post(authorized_client, test_post):
    res = authorized_client.get("/posts")

    assert res.status_code == 200


def test_getting_one_post(authorized_client, test_post):
    res = authorized_client.get("/posts/1")
    assert res.status_code == 200



def test_creating_post(authorized_client, test_user):

    post_data = {
            "title": "Title 1",
            "content": "Content number 1",
            "owner_id": test_user['id']
        }
    res = authorized_client.post("/posts", json=post_data)

    assert res.status_code == 201



def test_update_user(authorized_client, test_user, test_post):

    post_data = {
            "title": "Updated Title 1",
            "content": "Updated Content number 1",
            "owner_id": test_user['id']
        }
    res = authorized_client.put("/posts/1", json=post_data)

    assert res.status_code == 200



def test_delete_user(authorized_client, test_user, test_post):

    res = authorized_client.delete("/posts/1")

    assert res.status_code == 204
