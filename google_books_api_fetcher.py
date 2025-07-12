import requests


GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes?q=isbn:{}"


def fetch_book_information(isbn: str):
    books_info = requests.get(GOOGLE_BOOKS_API.format(isbn)).json()
    if books_info["totalItems"] == 0:
        return {}
    print(books_info)

    book_link = books_info["items"][0]["selfLink"]
    book_info = requests.get(book_link).json()
    volume_info = book_info["volumeInfo"]
    return volume_info
