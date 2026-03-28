from fastapi import FastAPI, Body


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Science"},
    {"title": "Title Three", "author": "Author Three", "category": "History"},
    {"title": "Title Four", "author": "Author Four", "category": "Math"},
    {"title": "Title Five", "author": "Author Two", "category": "Math"},
    {"title": "Title Six", "author": "Author Five", "category": "Math"},
]

app = FastAPI()

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/mybook")
async def read_my_book():
    return {"book_title": "My Favorite Book!"}

@app.get("/books/{book_title}")
async def read_all_books(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
        
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == book_author.casefold() and book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return                      

@app.get("/books/author/{author_name}")
async def get_author_books(author_name: str):
    get_all_books = []
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold():
            get_all_books.append(book)
    return get_all_books

@app.get("/books/author/get_books/")
async def get_author_books(author_name: str):
    get_all_books = []
    for book in BOOKS:
        if book.get("author").casefold() == author_name.casefold():
            get_all_books.append(book)
    return get_all_books

@app.post("/books/create_book")
async def creat_book(new_book = Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break