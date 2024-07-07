import pytest
import aiohttp
from ..utils import generate_random_email, generate_random_post_content, generate_random_post_title, login

random_email = generate_random_email()
random_title = generate_random_post_title()
random_content = generate_random_post_content()

curr_email = random_email
curr_title = random_title
curr_content = random_content

first_name = "Hayk"
last_name = "Ghazaryan"
password = "Password1!"

acc_id = None

BASE_URL = "https://api.ferny.xyz" 


@pytest.mark.asyncio
async def test_create_acc():

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        create_user_url = f"{BASE_URL}/users/"
        request_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": random_email,
            "password": password
        }

        # successful account creation
        async with session.post(create_user_url, json=request_data) as response:
            assert response.status == 201
            response_json = await response.json()
            assert request_data["first_name"] == response_json["first_name"]
            assert request_data["last_name"] == response_json["last_name"]
            assert curr_email == response_json["email"]
            assert type(response_json["id"]) == int



            # assigning the id to a var to use the account further
            global acc_id
            acc_id = response_json["id"]



@pytest.mark.asyncio
async def test_registered_email():

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:

        create_user_url = f"{BASE_URL}/users/"
        request_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": curr_email,
            "password": password
        }

        error_detail = "Email already registered"

        # email already registered
        async with session.post(create_user_url, json=request_data) as response:
            assert response.status == 400
            response_json = await response.json()
            
            assert error_detail == response_json["detail"]



@pytest.mark.asyncio
async def test_registration_without_required_values():

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:

        create_user_url = f"{BASE_URL}/users/"


        initial_request_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": random_email,
            "password": password
        }

        for key_to_skip in initial_request_data:
            request_data = {}
            for key, value in initial_request_data.items():
                if key != key_to_skip:
                    request_data[key] = value

                # checking if we receive the correct error when not sending the first_name
            async with session.post(create_user_url, json=request_data) as response:
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
async def test_get_account():

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        get_user_url = f"{BASE_URL}/users/{acc_id}"
        expected_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": curr_email,
            "password": password
        }

        # successful account creation
        async with session.get(get_user_url) as response:
            assert response.status == 200
            response_json = await response.json()
            assert expected_data["first_name"] == response_json["first_name"]
            assert expected_data["last_name"] == response_json["last_name"]
            assert expected_data["email"] == response_json["email"]
            assert type(response_json["id"]) == int


@pytest.mark.asyncio
async def test_update_acc():
    jwt_token = await login(curr_email, password)  

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        update_user_url = f"{BASE_URL}/users/"
        request_data = {
            "first_name": f"{first_name}_u",
            "last_name": f"{last_name}_u",
            "email": f"u_{curr_email}",
            "password": f"{password}U"
        }
        
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        for key_to_update in request_data:
            update_data = {key_to_update: request_data[key_to_update]}

            # successful account update
            async with session.patch(update_user_url, json=update_data, headers=headers) as response:
                assert response.status == 200
                response_json = await response.json()
                assert type(response_json["id"]) == int
                assert type(response_json["access_token"]) == str
                if key_to_update != "password":
                    assert update_data[key_to_update] == response_json[key_to_update]

         
@pytest.mark.asyncio
async def test_update_email_with_registered_email():
    jwt_token = await login(f"u_{curr_email}",  f"{password}U")  

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        update_user_url = f"{BASE_URL}/users/"
        request_data = { 
            "email": "hayykgh@gmail.com"
           }
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # successful account update
        async with session.patch(update_user_url, json=request_data, headers=headers) as response:
            assert response.status == 400
            response_json = await response.json()
            error_detail = "Email already registered"
            assert error_detail == response_json["detail"]


@pytest.mark.asyncio
async def test_delete_account():
    jwt_token = await login(f"u_{curr_email}",  f"{password}U")  

    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
        #  Create a new user
        delete_user_url = f"{BASE_URL}/users/{acc_id}"

        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }

        # successful account creation
        async with session.delete(delete_user_url, headers=headers) as response:
            assert response.status == 204