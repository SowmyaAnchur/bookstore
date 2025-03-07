import pytest
import httpx

url = "http://127.0.0.1:8000"
header = {"Authorization": "", "Content-Type": "application/json"}

book = {"id": 3,
        "name": "Romeo and Juliet",
        "author": "William Shakespeare",
        "published_year": "1597",
        "book_summary": "It is a tragic love story where the two main characters, Romeo and Juliet, are supposed "
                        "to be sworn enemies but fall in love"}

# This test is to verify creation of book and verifying it by get all books call
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

# This test is to verify  get all books call
@pytest.mark.integrationTest
@pytest.mark.getAllBooks
@pytest.mark.asyncio
async def test_getAllBooks(login):
    token = login
    header["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url + "/books/", headers=header)
        assert response.status_code == 200, print(f"Failed to get books. Error : {response.text}")
        getBooks = response.json()
        print("Retrieved all book details successfully")
        print(f"Books details:{getBooks}")


# This test is to verify get book
@pytest.mark.integrationTest
@pytest.mark.getBook
@pytest.mark.asyncio
async def test_getBookById(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient() as client:
        book_id = book['id']
        response = await client.get(url + "/books/" + str(book_id), headers=header)
        assert response.status_code == 200, print(f"Failed to get book by id. Error : {response.text}")
        print("Retrieved book details successfully")
        bookResponse = response.json()
        assert bookResponse["id"] == book_id, print("Book id is not same")
        print(f"Retrieved details of book id {book_id}")
        assert sorted(bookResponse) == sorted(book), print(f"Book details are incomplete")
        print("Book details are shown completely")


# This test is to verify update book
@pytest.mark.integrationTest
@pytest.mark.updateBook
@pytest.mark.asyncio
async def test_updateBookById(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient() as client:
        book_id = book['id']
        updatebook = {"published_year": 1876}
        book["published_year"] = 1876
        response = await client.put(url + "/books/" + str(book_id), json=updatebook, headers=header)
        assert response.status_code == 200, print(f"Failed to get book by id. Error : {response.text}")
        print("Retrieved book details successfully")
        bookResponse = response.json()
        assert bookResponse["published_year"] == updatebook["published_year"], print("Published year is not updated")
        print(f"Published year is updated")

        response = await client.get(url + "/books/" + str(book_id), headers=header)
        print("Retrieved book details successfully")
        bookResponse = response.json()
        assert bookResponse["published_year"] == updatebook["published_year"], print("Published year is not same in get book call")
        print(f"Retrieved details of book id {book_id}")
        print("Updated details are shown in get call")


# This test is to verify delete book
@pytest.mark.integrationTest
@pytest.mark.deleteBook
@pytest.mark.asyncio
async def test_deleteBookById(login):
    token = login
    header["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient() as client:
        book_id = book['id']
        response = await client.delete(url + "/books/" + str(book_id), headers=header)
        assert response.status_code == 200, print(f"Failed to delete book by id. Error : {response.text}")
        print("Deleted book successfully")
        responseData= response.json()
        assert responseData['message'] == "Book deleted successfully", print(f"Deleted message is incorrect")
        print("Deleted message is as expected")

        response = await client.get(url + "/books/", headers=header)
        getBooks = response.json()
        assert book not in getBooks, print(f"Get all books returned deleted book")
        print("Get all books dont contain deleted book")

