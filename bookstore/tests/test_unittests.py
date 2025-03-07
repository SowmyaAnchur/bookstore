import pytest
import requests

url = "http://127.0.0.1:8000"
header = {"Authorization": "", "Content-Type": "application/json"}

# This test is to verify login with valid credentials
@pytest.mark.unitTest
@pytest.mark.verifyLogin
@pytest.mark.asyncio
async def test_valid_userLogin(signup):
    userCreds = {"email": signup["email"], "password": signup["password"]}
    response = requests.post(url + "/login/", json=userCreds)
    assert response.status_code == 200, print(f"Login is not successful with valid credentials. Error: {response.text}")
    print("Login call is successful")


# This test is to verify login with invalid credentials
@pytest.mark.unitTest
@pytest.mark.verifyInvalidLogin
@pytest.mark.asyncio
async def test_invalid_userLogin(signup):
    userCreds = signup.copy()
    # Changing the password to wrong password
    userCreds['password'] = 'NoPassword'
    response = requests.post(url + "/login/", json=userCreds)
    assert response.status_code == 400, print(f"Login is successful with invalid credentials. Error: {response.text}")
    print("Got an expected status code for invalid user credentials")
    response = response.json()
    assert response['detail'] == 'Incorrect email or password'
    print("Got an expected response for invalid user credentials")


# This test is to verify creation of book
@pytest.mark.unitTest
@pytest.mark.createBook
@pytest.mark.asyncio
async def test_createBook(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    book = {"id": 1,
            "name": "Harry Potter",
            "author": "JK Rowling",
            "published_year": "1997",
            "book_summary": "Harry Potter is a series of novels by British author J. K. Rowling. The novels follow "
                            "Harry Potter, an 11-year-old boy who discovers he is the son of famous wizards and will "
                            "attend Hogwarts School of Witchcraft and Wizardry. Harry learns of an entire society of "
                            "wizards and witches."}
    response = requests.post(url + '/books', json=book, headers=header)
    assert response.status_code == 200, print(f"Failed to create book. Error : {response.text}")
    print("Created book successfully")


# This test is to verify update of book
@pytest.mark.unitTest
@pytest.mark.updateBook
@pytest.mark.asyncio
async def test_updateBook(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    book_id = 1
    book = {"book_summary": "Harry Potter is a series of novels by British author J. K. Rowling."}
    response = requests.put(url + '/books/' + str(book_id), json=book, headers=header)
    assert response.status_code == 200, print(f"Failed to update book. Error : {response.text}")
    print("Updated book successfully")


# This test is to verify update of book with non-existent book id
@pytest.mark.unitTest
@pytest.mark.updateNonExistentBook
@pytest.mark.asyncio
async def test_updateNonExistentBook(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    book_id = 999
    book = {"author": "William Shakespeare"}
    response = requests.put(url + '/books/' + str(book_id), json=book, headers=header)
    assert response.status_code == 404, print(f"Book updated successfully for non-existent book id. Error : {response.text}")
    print(f"Got expected 404 status")
    responseData = response.json()
    assert responseData["detail"] == "Book not found", print(
        f"Detail is not as expected, Message from API : {responseData['detail']}")
    print(f"Got expected 'Book Not Found' message")


# This test is to verify get books call
@pytest.mark.unitTest
@pytest.mark.getBooks
@pytest.mark.asyncio
async def test_getBooks(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    response = requests.get(url + '/books', headers=header)
    assert response.status_code == 200, print(f"Failed to get all books. Error : {response.text}")
    print("Retrieved all books successfully")


# This test is to verify get book by id
@pytest.mark.unitTest
@pytest.mark.getBookById
@pytest.mark.asyncio
async def test_getBookById(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    book_id = 1
    response = requests.get(url + '/books/' + str(book_id), headers=header)
    assert response.status_code == 200, print(f"Failed to get book of id {book_id}. Error : {response.text}")
    print(f"Retrieved book with id {book_id} successfully")


# This test is to verify get book by non-existent id
@pytest.mark.unitTest
@pytest.mark.getBookByNonExistentId
@pytest.mark.asyncio
async def test_getBookByNonExistentId(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    book_id = 999
    response = requests.get(url + '/books/' + str(book_id), headers=header)
    assert response.status_code == 404, print(f"Retrieved book successfully for non-existent book id. Error : {response.text}")
    print(f"Got expected 404 status")
    responseData = response.json()
    assert responseData["detail"] == "Book not found", print(f"Detail is not as expected, Message from API : {responseData['detail']}")
    print(f"Got expected 'Book Not Found' message")


# This test is to verify delete of book
@pytest.mark.unitTest
@pytest.mark.deleteBook
@pytest.mark.asyncio
async def test_deleteBook(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    book_id = 1
    response = requests.delete(url + '/books/' + str(book_id), headers=header)
    assert response.status_code == 200, print(f"Failed to delete book. Error : {response.text}")
    print("Deleted book successfully")


# This test is to verify delete book by non-existent id
@pytest.mark.unitTest
@pytest.mark.deleteBookByNonExistentId
@pytest.mark.asyncio
async def test_deleteBookByNonExistentId(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    book_id = 999
    response = requests.delete(url + '/books/' + str(book_id), headers=header)
    assert response.status_code == 404, print(f"Deleted book successfully for non-existent book id. Error : {response.text}")
    print(f"Got expected 404 status")
    responseData = response.json()
    assert responseData["detail"] == "Book not found", print(
        f"Detail is not as expected, Message from API : {responseData['detail']}")
    print(f"Got expected 'Book Not Found' message")

