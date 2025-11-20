from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from parses.pdf_parser import extract_text_from_pdf
from parses.docx_parser import extract_text_from_doc
from jobMatch import match_jobs, extract_skills
from webScrape import jobs_scrape_and_update
from apscheduler.schedulers.background import BackgroundScheduler
import sys

app = FastAPI()
scheduler = BackgroundScheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


scheduler.add_job(jobs_scrape_and_update, "interval", minutes=720)
scheduler.start()

@app.post("/match")
async def match_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(contents)
        elif file.filename.endswith(".docx"):
            text = extract_text_from_doc(contents)
        else:
            return JSONResponse(status_code=400, content={"error": "Only PDF or DOCX allowed"})

        user_skills = extract_skills(text)
        matches = match_jobs(user_skills)

        # Debug
        print("Extracted Skills:", user_skills, file=sys.stdout, flush=True)
        print("Total Matches:", len(matches), file=sys.stdout, flush=True)

        return {
            "extracted_skills": user_skills,
            "matches": matches
        }

    except Exception as e:
        print("Error in match_resume:", e, file=sys.stdout, flush=True)
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def root():
    return {"status": "ok"}
