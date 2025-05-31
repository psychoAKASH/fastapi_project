from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_books():
    return {"hi there"}
