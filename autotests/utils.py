import random

import string

import aiohttp
import pytest


BASE_URL = "https://api.ferny.xyz" 


def generate_random_email(domain="yopmail.com", length=10):
    letters = string.ascii_letters + string.digits
    username = ''.join(random.choice(letters) for _ in range(length))
    return f"aqa+{username}@{domain}"

def generate_random_post_title(length=10):
    letters = string.ascii_letters + string.digits
    title = ''.join(random.choice(letters) for _ in range(length))
    return f"title: {title}"

def generate_random_post_content(length=30):
    letters = string.ascii_letters + string.digits
    content = ''.join(random.choice(letters) for _ in range(length))
    return f"content: {content}"

random_email = generate_random_email()
random_title = generate_random_post_title()
random_content = generate_random_post_content()

curr_email = random_email
curr_title = random_title
curr_content = random_content

first_name = "Hayk"
last_name = "Ghazaryan"
password = "Password1!"

async def create_acc():

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
            response = await response.json()
            return response["id"]

async def login(email, password):
    async with aiohttp.ClientSession() as session:

        login_url = f"{BASE_URL}/login/"
        form_data = aiohttp.FormData()
        form_data.add_field('username', email)
        form_data.add_field('password', password)


        async with session.post(login_url, data=form_data) as response:
            response_json = await response.json()
            jwt = response_json["access_token"]
            return jwt
        
async def create_post():
    jwt_token = await login(curr_email, password)  
    # Use aiohttp to test the backend
    async with aiohttp.ClientSession() as session:
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
            response_json = await response.json()
            return response_json["id"]
        


async def create_votes():
    jwt_token = await login(curr_email, password)
    post_ids = {}
    headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
    async with aiohttp.ClientSession() as session:
        for i in range(5):
            post_id = await create_post()
            create_vote_url = f"{BASE_URL}/vote/{post_id}"
            
            async with session.post(create_vote_url, headers=headers) as response:
                post_ids[f'post_id_{i}'] = post_id

    return post_ids