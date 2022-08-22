from fastapi import FastAPI, Response, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import Optional, List
import shutil

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

@app.post("/uploadfiles")
async def get_file(response: Response, files: List[UploadFile]):
    response.headers["Access-Control-Allow-Origin"] = "*"
    path = f'C:/Users/maron/text/{files[0].filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(files[0].file, buffer)
    f = open(path, 'r')
    lines = f.readlines()
    return lines
    # contents = await files[0].read()
    # contents = contents.decode('utf-8')
    # lines = contents.split('\r\n')
    # return {'filename': filename, 'content': contents}
