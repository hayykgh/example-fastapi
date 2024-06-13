def test_vote_adding(authorized_client, test_user, test_post):

    res = authorized_client.post("/vote/1")

    assert res.status_code == 200



def test_vote_removing(authorized_client, test_user, test_post):

    res = authorized_client.post("/vote/1")

    assert res.status_code == 200