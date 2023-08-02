from fakegenerator import FakeGenerator
from file_exporter import File_Exporter
from sql_exporter import SQL_exporter
from web_exporter import Web_exporter
import os
from typing import List
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
current_directory = os.path.dirname(os.path.realpath(__file__))
static_directory = os.path.join(current_directory, "static")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
f_exp = File_Exporter()
web_exp = Web_exporter()

path_to_save = Path("./static/generated_content/")
csv_path = path_to_save / "out.csv"
json_path = path_to_save / "out.json"
xls_path = path_to_save / "out.xls"
lsql_name = "out"

sql_exp = SQL_exporter(db_path=path_to_save, db_name=lsql_name)

@app.get("/")
async def root(request: Request):  # Добавьте request как аргумент
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate/")
async def generate(
    data: List[str] = Form(...),
    sex: List[str] = Form(...),
    country: List[str] = Form(...),
    min_age: int = Form(...),
    max_age: int = Form(...),
    file_types: List[str] = Form(...),
    value:int = Form(...)
    ):
    """
    Пока генерация идёт в сессии файлы дописываются, если перезапустить сервер предыдущая генерация будет удалена.
    """
    
    #======Delete previus files in directory===
    for file in path_to_save.iterdir():
        if file.is_file():
            file.unlink()
    
    models_in_req = []
    
    for _ in range(value):
        f_g = FakeGenerator(sex=sex, age=[min_age, max_age], country=country)
        for x in data:
            models_in_req.append(getattr(f_g.generator, x, None)())
    
    for mod in models_in_req:
        f_exp.buffer.add(mod)
        sql_exp.buffer.add(mod)
    
    
    for f_t in file_types:
        if f_t == "JSON":
            f_exp.json(path_json=json_path)
        elif f_t == "CSV":    
            f_exp.csv(save_to_string=True, path_csv=csv_path)
        elif f_t == "XLS":
            f_exp.xls(path_xls= xls_path)    
        elif f_t == "LiteSQL":
            sql_exp.dump_data(sql_buffer=sql_exp.buffer.buf)
    
    urls = {}
    
    for url in file_types:
        if url == "CSV":
            urls[url] = str(csv_path)       
        elif url == "JSON":
            urls[url] = str(json_path)
        elif url == "XLS":
            urls[url] = str(xls_path)   
        elif url == "LiteSQL": 
            urls[url] = str(path_to_save / lsql_name)
    return urls

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)