import os
from pathlib import Path
from chain_builder import Window
import uvicorn
from config import file_upload_delete
import fastapi
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from data_preparing import embedding,cache_embedding
app = FastAPI()
embedding = embedding()
cache_embedding = cache_embedding(embedding)
store = {}
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    save_path = Path(file_upload_delete)
    file_path = save_path/file.filename
    with open(file_path, "wb") as file_on_disk:
        file_on_disk.write(await file.read())
    return {"filename": file.filename, "saved_at": file_path}



@app.post("/delete")
async def delete_file(file: str = Form(...)):
        DIR_path = Path(file_upload_delete).resolve()
        file_path = DIR_path/file
        if not file_path.is_file():
            raise HTTPException(404, "文件不存在")
        if not file_path.resolve().relative_to(DIR_path.resolve()):
            raise HTTPException(404,"非法路径")
        file_path.unlink()
        return {"delete_filename": file,"delete":"successfully deleted"}
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/rag")
async def chat(
        input: str = Form(...),
        id: str = Form(...),
):
    if id not in store:
        store[id] = Window(id,embedding,cache_embedding)
    res = await store[id].run_api(input)
    return {
        "id": id,
        "result": res
    }



uvicorn.run(app, host="localhost", port=8000)


