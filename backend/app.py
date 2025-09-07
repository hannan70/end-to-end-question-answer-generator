from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import csv
import os
import aiofiles
import glob
from src.helper import llm_pipeline

app = FastAPI(
    title="Question Answer Generator"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)


# upload file
@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    # file uploaded base directory
    upload_dir = "static/uploads"
    # if directory not exists then create new dir
    if not os.path.isdir(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
     
    # if exists the any file then remove the file
    existing_files = glob.glob(os.path.join(upload_dir, "*"))
    for f in existing_files:
        os.remove(f)

    # save pdf in upload dir
    file_path = os.path.join(upload_dir, file.filename)
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # pass the llm
    llm_pipeline(file_path)

    return JSONResponse(content={
        "filename": file.filename,  
        "file_path": file_path,
        "message": "file uploaded successfully"
    })


@app.get('/csv-file')
async def get_csv_file():
    uploaded_dir = 'static/output'
    full_path = os.path.join(uploaded_dir, 'question_answer.csv')

    if not os.path.exists(full_path):
        return {"error": "File not found"}
    
    return FileResponse(
        path=full_path,
        media_type="text/csv",
        filename="question_answer.csv"
    )

@app.get('/json-file')
async def get_json_file():
    uploaded_dir = 'static/output'
    full_path = os.path.join(uploaded_dir, 'question_answer.json')

    if not os.path.exists(full_path):
        return {"error": "File not found"}
    
    return FileResponse(
        path=full_path,
        media_type="text/csv",
        filename="question_answer.json"
    )

# get all question and answer from csv
@app.get('/all-data')
async def get_all_question_answer():
    results = []
    uploaded_dir = 'static/output'
    full_path = os.path.join(uploaded_dir, 'question_answer.csv')

    if not os.path.exists(full_path):
        return {"error": "File not found"}
    
    with open(full_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        for row in reader:
            results.append({
                "Question": row.get("Question"),
                "Answer": row.get("Answer")
            })

    return {"data": results}
