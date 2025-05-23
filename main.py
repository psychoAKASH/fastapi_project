from fastapi import FastAPI

app = FastAPI()


@app.get('/books')
def read_books():
    return {"hi there"}
