
from pathlib import Path
from GitHub_Prepared_Rag.Core.chain_builder import Window
import uvicorn
from GitHub_Prepared_Rag.Config.config import file_upload_delete
from Model.models import *
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Body
from Core.RAGManager import RagManager
manager = RagManager()
store = {}
app = FastAPI()
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


@app.post("/chat_with_rag")
async def chat(info : chat = Body(...)):
    if info.id not in store:
        store[info.id] = Window(manager=manager,id=info.id,is_async=True)
    res = await store[info.id].run_api(info.input)
    return {
        "id": info.id,
        "result": res
    }



uvicorn.run(app, host="localhost", port=8000)