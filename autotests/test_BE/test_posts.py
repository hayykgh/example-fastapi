import pytest
import aiohttp
from ..utils import generate_random_post_content, generate_random_post_title, login, create_acc, curr_email

random_title = generate_random_post_title()
random_content = generate_random_post_content()

curr_title = random_title
curr_content = random_content

first_name = "Hayk"
last_name = "Ghazaryan"
password = "Password1!"

BASE_URL = "https://api.ferny.xyz" 


post_id = None
owner_id = None

@pytest.mark.asyncio
async def test_create_post():
    post_owner_id = await create_acc()
    jwt_token = await login(curr_email, password)  
    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        create_post_url = f"{BASE_URL}/posts/"
        request_data = {
        "title": random_title,
        "content": random_content
        }

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
        # successful post creation
        async with session.post(create_post_url, json=request_data, headers=headers) as response:
            assert response.status == 201
            response_json = await response.json()
            assert request_data["title"] == response_json["title"]
            assert request_data["content"] == response_json["content"]
            assert True == response_json["published"]
            assert int == type(response_json["id"])
            assert  post_owner_id == response_json["owner_id"]

            global post_id, owner_id
            post_id = response_json["id"]
            owner_id = post_owner_id


@pytest.mark.asyncio
async def test_post_without_required_values():
    jwt_token = await login(curr_email, password)  

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:

        create_post_url = f"{BASE_URL}/posts/{post_id}"


        initial_request_data = {
            "title": curr_title,
            "content": curr_content,
        }


        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        for key_to_skip in initial_request_data:
            request_data = {}
            for key, value in initial_request_data.items():
                if key != key_to_skip:
                    request_data[key] = value

                # checking if we receive the correct error when not sending the first_name
            async with session.put(create_post_url, json=request_data, headers=headers) as response:
                assert response.status == 422
                response_json = await response.json()
                
                detail = response_json["detail"][0]
                
                # checks that the type has a "missing" value 
                assert detail["type"] == "missing"

                # checks that the loc indicates which values are missing 
                assert detail["loc"][0] == "body"
                assert detail["loc"][1] == key_to_skip

                # checks that the msg has a "Field required" value 
                assert detail["msg"] == "Field required"

                # checks that the input array contains what was sent in the request 
                assert detail["input"] == request_data


@pytest.mark.asyncio
async def test_get_post():
    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        get_post_url = f"{BASE_URL}/posts/{post_id}"

        # successful account creation
        async with session.get(get_post_url) as response:
            assert response.status == 200
            response_json = await response.json()
            response_json = response_json["Post"]
            assert curr_title == response_json["title"]
            assert curr_content == response_json["content"]
            assert True == response_json["published"]
            assert post_id == response_json["id"]
            assert  owner_id == response_json["owner_id"]


@pytest.mark.asyncio
async def test_update_post():
    jwt_token = await login(curr_email, password)  

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        update_post_url = f"{BASE_URL}/posts/{post_id}"
        request_data = {
            "title": f"{curr_title}_u",
            "content": f"{curr_content}_u",
        }
        
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

            # successful account update
        async with session.put(update_post_url, json=request_data, headers=headers) as response:
            assert response.status == 200
            response_json = await response.json()
            assert request_data["title"] == response_json["title"]
            assert request_data["content"] == response_json["content"]
            assert True == response_json["published"]
            assert post_id == response_json["id"]
            assert owner_id == response_json["owner_id"]




@pytest.mark.asyncio
async def test_delete_post():
    jwt_token = await login(curr_email, password)  

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        delete_post_url = f"{BASE_URL}/posts/{post_id}"

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # successful account creation
        async with session.delete(delete_post_url, headers=headers) as response:
            assert response.status == 204

            