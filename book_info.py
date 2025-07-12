import date


class Book_info:
    def __init__(self, isbn: str, title: str, authors: list, publisher: str, published_date: date, printed_page_count: int, dimensions: {}, maturity_rating: str, language: str):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.published_date = published_date
        self.printed_page_count = printed_page_count
        self.dimensions = dimensions
        self.maturity_rating = maturity_rating
        self.language = language
