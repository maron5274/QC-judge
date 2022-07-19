from fastapi import FastAPI, Response, File, UploadFile
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
