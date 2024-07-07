import pytest
import aiohttp
from ..utils import curr_email, password


BASE_URL = "https://api.ferny.xyz" 


@pytest.mark.asyncio
async def test_login():
    async with aiohttp.ClientSession() as session:

        login_url = f"{BASE_URL}/login1/"
        form_data = aiohttp.FormData()
        form_data.add_field('username', curr_email)
        form_data.add_field('password', password)


        async with session.post(login_url, data=form_data) as response:
            
            response_json = await response.json()

            assert response.status == 200
            assert type(response_json["access_token"]) == str
            assert response_json["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_with_incorrect_pass():
    async with aiohttp.ClientSession() as session:
        loginerror = "Invalid credentials"
        login_url = f"{BASE_URL}/login/"
        form_data = aiohttp.FormData()
        form_data.add_field('username', curr_email)
        form_data.add_field('password', f"{password}In")


        async with session.post(login_url, data=form_data) as response:
            
            response_json = await response.json()

            assert response.status == 403
            assert response_json["detail"] == loginerror

@pytest.mark.asyncio
async def test_login_with_incorrect_email():
    async with aiohttp.ClientSession() as session:
        loginerror = "Invalid credentials"
        login_url = f"{BASE_URL}/login/"
        form_data = aiohttp.FormData()
        form_data.add_field('username', f"in{curr_email}")
        form_data.add_field('password', password)


        async with session.post(login_url, data=form_data) as response:
            
            response_json = await response.json()

            assert response.status == 403
            assert response_json["detail"] == loginerror
