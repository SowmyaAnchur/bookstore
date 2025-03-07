# Bookstore API

## Overview

This project is a **bookstore** application with **unit tests**, **integration tests**, and a **Jenkins pipeline** configuration to run these tests. The application uses **FastAPI** as the framework, and **pytest** for testing.

## Unit Tests

Unit tests are used to validate the functionality of individual API calls in isolation. In this project, we use the **pytest** framework for writing and running unit tests.

### Example Unit Test

Here’s an example of a simple unit test for a FastAPI application:

```python
# test_unittests.py

@pytest.mark.unitTest
@pytest.mark.getBooks
@pytest.mark.asyncio
async def test_getBooks(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    response = requests.get(url + '/books', headers=header)
    assert response.status_code == 200, print(f"Failed to get all books. Error : {response.text}")
    print("Retrieved all books successfully")
```

## Integration Tests

Integration tests check how various API calls of the application work together.

### Example Integration Test

Here’s an example of a simple integration test for a FastAPI application:

```python
# test_integrationtests.py

@pytest.mark.integrationTest
@pytest.mark.createBook
@pytest.mark.asyncio
async def test_createBook(login):
    token = login
    header["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        response = await client.post(url + "/books/", json=book, headers=header)
        assert response.status_code == 200, print(f"Failed to create book. Error : {response.text}")
        print("Created book successfully")
        bookResponse = response.json()
        assert sorted(bookResponse) == sorted(book), print(f"Created book is different from data sent")
        print("Book is created according to data sent")
        response = await client.get(url + "/books/", headers=header)
        getBooks = response.json()
        assert bookResponse in getBooks, print(f"Get all books didn't return created book")
        print("Get all books contain created book")
```

## Jenkins Pipeline Configuration

This project includes a JenkinsFile to automate the testing process. The JenkinsFile defines the steps to build, test, and deploy the application.

### Jenkins file location and explanation

#### Checkout
This stage clones the code from a GitHub repository.
#### Set up Python Environment
It sets up a Python virtual environment and installs dependencies from requirements.txt.
#### Run Unit Tests
This step runs unit tests using pytest.
#### Run Integration Tests
This step runs integration tests using pytest.
#### Post Actions
Displays messages depending on whether the tests pass or fail and stops the uvicorn process.


### Running the Jenkins Pipeline

Create a Jenkins project that pulls the repository where the Jenkinsfile is stored.
Ensure that the Jenkins agent has Python installed.
Configure the project to use the Jenkinsfile in the repository.


### Running Locally

Ensure that python is installed on the system

Clone the repository https://github.com/SowmyaAnchur/bookstore.git

Navigate to bookstore directory and create venv: cd bookstore && python -m venv venv

Install the requirements: pip install -r requirements.txt

Start the API server: uvicorn main:app --reload

In a new terminal follow above steps except starting server and run the commands: pytest -m unitTest --html=unitTests.html  for unit tests
pytest -m integrationTest --html=integrationTests.html  for unit tests for integration tests

## Testing approach:

Sessions are managed by separating the signup and login processes in conftest.py. The signup process is executed once per session to generate a Bearer token, which is then reused for the duration of the session, ensuring efficient authentication for subsequent requests.

Each test includes assertions to verify expected outcomes and HTTP response codes, helping to ensure the correctness of the system. Negative test cases are also included to check how the system handles invalid inputs and unexpected scenarios.

For improved readability and maintainability, all tests are named according to the functionality they verify.

Tests are designed to exit immediately if any errors occur, ensuring that the failure of one test does not impact the execution of subsequent tests.

Logs are structured in a way that provides clear insights into failures, making debugging and issue resolution more efficient.

### Unit tests:

Unit tests are designed to validate individual API endpoints in isolation, ensuring both positive and negative scenarios are handled correctly. These tests focus on verifying the functionality of key operations such as login and all CRUD (Create, Read, Update, Delete) operations, ensuring that each behaves as expected under different conditions.

### Integration tests:

Integration tests focus on evaluating how multiple API calls interact within the system. These tests ensure that components work together as expected and validate end-to-end functionality.



