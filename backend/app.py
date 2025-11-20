from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from parses.pdf_parser import extract_text_from_pdf
from parses.docx_parser import extract_text_from_doc
from jobMatch import match_jobs
from pathlib import Path
from webScrape import jobs_scrape_and_update
from apscheduler.schedulers.background import BackgroundScheduler
from jobMatch import extract_skills
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
scheduler = BackgroundScheduler()


# List of all allowed origins
origins = [
    "https://resume-to-job-matcher.vercel.app",  
    "https://*.vercel.app",  
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

# Allow react frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app",  # Allows all Vercel deployments
    allow_origins=[
        "https://resume-to-job-matcher.vercel.app",
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run scrape function automatically for every 12 hrs
scheduler.add_job(jobs_scrape_and_update, "interval", hours =12)
scheduler.start()




@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(contents)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_doc(contents)
        else:
            return {"error": "only PDF or DOCX file supported"}
        
        return {"filename": file.filename, "extracted_text": text}
    except Exception as e:
        print(f"Error in upload_resume: {e}")
        return {"error": str(e)}, 500


# Endpoint to both upload pdf/docx and match with jobs
@app.post("/match")
async def match_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(contents)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_doc(contents)
        else:
            return {"error": "only PDF or DOCX file supported"}
        
        user_skills = extract_skills(text)
        matches = match_jobs(user_skills)

        return {
            "extracted_skills": user_skills,
            "matches": matches
        }
    except Exception as e:
        print(f"Error in match_resume: {e}")
        return {"error": str(e)}, 500


# Health check endpoint
@app.get("/")
async def root():
    return {"status": "ok", "message": "Resume to Job Matcher API"}

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()