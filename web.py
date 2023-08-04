#========Import DPDG classes for data generation====#
from fakegenerator import FakeGenerator
from file_exporter import File_Exporter
from sql_exporter import SQL_exporter

#========Import libraries for path manipulation and typing====#
import os
from pathlib import Path
from typing import List, Dict, Callable

#========Import FAST API and Jinja2 for web application setup=======#
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

#===============Initialize FAST API and configure the static files directory======#
app = FastAPI()
current_directory = os.path.dirname(os.path.realpath(__file__)) #Take current dir position.
static_directory = os.path.join(current_directory, "static") # Move to static underfolder.
app.mount("/static", StaticFiles(directory="static"), name="static") #Mount full path to static folder.
templates = Jinja2Templates(directory="templates") #Set up the directory with html templates.

#======Initialize DPDG generator classes======#
f_exp = File_Exporter()

#========Define paths to save generated data======#
path_to_save = Path("./static/generated_content/")
csv_path = path_to_save / "out.csv"
json_path = path_to_save / "out.json"
xls_path = path_to_save / "out.xls"
lsql_name = "out"


#=======Initialize SQL Exporter class and configure it.======#
sql_exp = SQL_exporter(db_path=path_to_save, db_name=lsql_name)




#========Main zone of web application set up===========================# 
def reset_previuse_data() -> bool:
    """
    Deletes all files in the folder with generated data.

    This function is used before the web application starts and when the reset button 
    in the web application is clicked.

    Returns:
        bool: Always returns True after successfully deleting the files.
    """
    for file in path_to_save.iterdir():
        if file.is_file():
            file.unlink()
    return True 

@app.get("/")
async def root(request: Request):
    """
    Handles the root endpoint of the application and serves the index.html template.
    
    It first resets any previous data before rendering the template.
    
    Args:
        request (Request): The incoming request object provided by FastAPI.
        
    Returns:
        TemplateResponse: Rendered index.html template with request context.
    """
    reset_previuse_data()
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate/")
async def generate(
    data: List[str] = Form(...),       # List of data models to be generated.
    sex: List[str] = Form(...),        # Sex parameters for data generation.
    country: List[str] = Form(...),    # Country parameters for data generation.
    min_age: int = Form(...),          # Minimum age for data generation.
    max_age: int = Form(...),          # Maximum age for data generation.
    file_types: List[str] = Form(...), # File formats to which data should be exported.
    value:int = Form(...)              # Number of data generation iterations (number of rows).
    ) -> Dict[str,str]:
    """
    Generates data based on given parameters and exports it to specified file formats.
    
    Args:
        data (List[str]): Models to generate data for.
        sex (List[str]): Sex parameter(s) for data generation.
        country (List[str]): Country parameter(s) for data generation.
        min_age (int): Minimum age for generated data.
        max_age (int): Maximum age for generated data.
        file_types (List[str]): Desired export formats for generated data.
        value (int): Number of data generation iterations.

    Returns:
        Dict[str, str]: Dictionary containing URLs of generated files for each format.
    """
    
    models_in_req = []
    
    #=====Main data generation loop====#
    for _ in range(value):
        f_g = FakeGenerator(sex=sex, age=[min_age, max_age], country=country)
        for x in data:
            models_in_req.append(getattr(f_g.generator, x, None)())
    
    #=====Adding generated data to buffers===#
    for mod in models_in_req:
        f_exp.buffer.add(mod)
        sql_exp.buffer.add(mod)
    
    #====Export generated data to specified file formats===#
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
    
    #========Create URLs for exported data files======#
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


@app.post("/reset/")
async def reset() -> bool:
    """
    Endpoint to reset or clear previously generated data.

    Returns:
        bool: The result of the reset operation, typically True if successful.
    """
    return reset_previuse_data()
            
# Check if the script is executed directly (not imported)
if __name__ == "__main__":
    # Import the Uvicorn server
    import uvicorn
    
    # Run the FastAPI app using Uvicorn
    # The application will be available at http://0.0.0.0:8000/
    uvicorn.run(app, host="0.0.0.0", port=8000)