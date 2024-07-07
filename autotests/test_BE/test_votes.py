import pytest
import aiohttp
from ..utils import  login,  curr_email, password, create_post, create_votes

added_message = "Successfully added the vote"
removed_message = "Successfully deleted the vote"
added = 1
removed = 0

BASE_URL = "https://api.ferny.xyz" 

@pytest.mark.asyncio
async def test_create_vote():
    jwt_token = await login(curr_email, password)
    post_id = await create_post()
    
    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        create_vote_url = f"{BASE_URL}/vote/{post_id}"

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
        # successful vote creation
        async with session.post(create_vote_url, headers=headers) as response:
            assert response.status == 200
            response_json = await response.json()
            assert added_message == response_json["message"]
            assert added == response_json["likes"]

        # successful vote deletion
        async with session.post(create_vote_url, headers=headers) as response:
            assert response.status == 200
            response_json = await response.json()
            assert removed_message == response_json["message"]
            assert removed == response_json["likes"]



@pytest.mark.asyncio
async def test_get_votes():
    jwt_token = await login(curr_email, password)
    votes = await create_votes()

    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        get_vote_url = f"{BASE_URL}/vote/"

        # Fetch votes
        async with session.get(get_vote_url, headers=headers) as response:
            response_json = await response.json()
            for i in range(len(votes)):
                assert response_json[i]["postid"] == votes[f"post_id_{i}"]
            assert response.status == 200