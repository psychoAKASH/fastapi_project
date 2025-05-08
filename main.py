from fastapi import FastAPI

app = FastAPI()


class Books:
    id: int
    author: str
    title: str
    rating: int

    def __init__(self, id, author, title, rating):
        self.id = id
        self.author = author
        self.title = title
        self.rating = rating


Books = [
    Books(1, 'Ak', 'Seven wonder of the worlds', 4),
    Books(2, 'ka', 'Seven deadly sins', 2),
    Books(3, 'yo', 'one piece', 5),
    Books(4, 'yum', 'dumb ways to die', 4)

]


@app.get('/books')
def read_books():
    return Books
