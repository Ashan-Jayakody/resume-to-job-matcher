from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from parses.pdf_parser import extract_text_from_pdf
from parses.docx_parser import extract_text_from_doc
from jobMatch import match_jobs
from pathlib import Path
from webScrape import jobs_scrape_and_update
from apscheduler.schedulers.background import BackgroundScheduler
from jobMatch import extract_skills

app = FastAPI()
scheduler = BackgroundScheduler()

# Allow react frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
        ],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run scrape function automatically for every 12 hrs
scheduler.add_job(jobs_scrape_and_update, "interval", hours =12)
scheduler.start()




@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    contents = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(contents)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_doc(contents)
    else:
        return {"error":"only PDF or DOCX file supported"}
    
    return {"filename": file.filename, "extracted_text": text}


# Endpoint to both upload pdf/docx and match with jobs
@app.post("/match")
async def match_resume(file: UploadFile = File(...)):
    contents = await file.read()

    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(contents)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_doc(contents)
    else:
        return {"error":"only PDF or DOCX file supported"}
    
    user_skills = extract_skills(text)
    matches = match_jobs(user_skills)

    return{
        "extracted_skills": user_skills,
        "matches": matches
    }