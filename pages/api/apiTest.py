from fastapi import FastAPI, Response, File
from typing import Optional

app = FastAPI()

@app.get("/")
def read_root(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"Hello": "World"}

@app.post('/file')
def get_file(response: Response, file: bytes = File(...)):
    response.headers["Access-Control-Allow-Origin"] = "*"
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {'lines': lines}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

# @app.get("/booklist")
# def read_books():
#     books = [
#         {'name': 'book1', 'price': 1500},
#         {'name': 'book2', 'price': 1800},
#         {'name': 'book3', 'price': 2300},
#     ]
#     return books