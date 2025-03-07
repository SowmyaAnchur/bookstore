import pytest
import random
import requests
import string

url = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def signup():
    chars = string.ascii_lowercase + string.digits
    username = "".join(random.choice(chars) for x in range(7))
    email = username + '@sample.com'
    password = "".join(random.choice(chars) for x in range(12))
    requestbody = {"email": f"{email}", "password": f"{password}"}
    response = requests.post(url + '/signup', json=requestbody)
    if response.status_code == 200:
        print("Created user successfully")
        return requestbody
    else:
        pytest.fail(f"Failed to create user. Error : {response.text}")


@pytest.fixture()
def login(signup):
    response = requests.post(url + '/login', json=signup)
    jsonResponse = response.json()
    if response.status_code == 200:
        print(f"User {signup['email']} logged in successfully")
        return jsonResponse["access_token"]
    else:
        pytest.fail(f"Login failed for user {signup['email']}. Error : {response.text}")
