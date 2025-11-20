# Resume-to-job-matcher
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18-blue)
![PostgreSQL](https://img.shields.io/badge/Postgres-12+-green)


This is a web application that matches resumes with job oppotunities by analyzing skills and requirements.
This web application features automated job data scraping by local job posting sites, resume parsing capabilities and matching algorithms,
all built with modern tech stack including React frontend, Python backend, and PostgreSQL database.

### 🎯Goal: Demonstrate an end to end skills matching system as a learning/MVP project.

## Features (MVP)
+ Web scraping: Automated job data fetching from local job posting sites (via approved APIs or scraping where permitted).
+ Resume parsing: Upload and parse PDF and DOCX resume files to extract key skills & experience.
+ Matching algorithm: To rank job postings by skills overlap.
+ PostgreSQL database: Robust data storage for job postings and matching results.
+ Modern UI: React based frontend with responsive design.


## 🌐Live Demo
### Quick Start - Try it live:
1. Visit the live app on: https://resume-to-job-matcher-9qjx9n978-ashan-jayakodys-projects.vercel.app
2. Upload your resume in PDF or DOCX format
3. Get instant job matches based on your skills.

> [! NOTE ]   
> The backend is deployed on Render's free tier and may take 30-60 seconds to wake up from sleep mode on the first request.
<img width="1800" height="925" alt="Screenshot 2025-09-30 135909" src="https://github.com/user-attachments/assets/f10a0542-5450-4a08-b3ff-41c5305c612f" />
<img width="1919" height="925" alt="Screenshot 2025-09-30 140641" src="https://github.com/user-attachments/assets/f8c76951-0244-45b0-a342-abc4da6b74f8" />
<img width="1919" height="930" alt="Screenshot 2025-09-30 140705" src="https://github.com/user-attachments/assets/bc88f45e-3a4f-4910-943d-6c3af5b78ce3" />


## Deployment
The application is deployed using modern cloud platforms.
+ Frontend: Depoloyed on Vercel for optimal React performance.
+ Backend: Deployed on Render with automatic scaling.
+ Database: PostgreSQL hosted on Render.

> [! TIP ]\
> Deployment Architecture \
> Frontend (Vercel) → Backend API (Render) → PostgreSQL Database (Render)


# Local Development / Test setup
If you want to run this application locally for development or testing:

## 📋Prerequisites foor local development
Before running this application, make sure you have following installed 
+ Node.js(v16 or higher)
+ Python(v3.8 or higher)
+ PostgreSQL(v12 or higher)
+ Git


## 💻Local Installing steps

1. Clone the Repository
   ```text
     - git clone https://github.com/yourusername/resume-to-job-matcher.git
     - cd resume-to-job-matcher
   ```
2. Backend setup
   ```bash
     - cd backend                             # Create a virtual environment (recommended)
     - python -m venv resume_matcher_env      # Activate virtual env on Windows:
     - resume_matcher_env\Scripts\activate    # Activate virtual env on Mac OS/Linux:
     - source resume_matcher_env/bin/activate # Install python dependencies
     - pip install -r requirements.txt        # Create .env file for local dev
     - touch .env
   ```
   
  3. Configure Local Environment
     ```bash
     # Local PostgreSQL Configuration:
        > DATABASE_URL=postgresql://username:password@localhost:5432/resume_job_matcher

     # Or individual database settings:
        > DB_HOST=localhost
        > DB_PORT=5432
        > DB_NAME=resume_job_matcher
        > DB_USER=your_username
        > DB_PASSWORD=your_password
     ```
   5. Database Setup (PostgreSQL)
      ```bash
      # Connect to PostgreSQL and create database
        > CREATE DATABASE resume_job_matcher;
      # Connect to the database and create the jobs table
        > \c resume_job_matcher;

        > CREATE TABLE IF NOT EXISTS public.jobs\
        > (\
        >     link text COLLATE pg_catalog."default" NOT NULL,\
        >     title text COLLATE pg_catalog."default" NOT NULL,\
        >     description text COLLATE pg_catalog."default",\
        >     company text COLLATE pg_catalog."default",\
        >     location text COLLATE pg_catalog."default",\
        >     CONSTRAINT jobs_pkey PRIMARY KEY (link)\
        > );

      ** Or use __pgAdmin4__ as PostgreSQL management interface.
      ```
  7. Frontend Setup
     ```bash
        > cd frontend/my-app\
        > npm install
     ```
      To install [Tailwind css as a vite plugin](https://tailwindcss.com/docs/installation/using-vite)
   
  9. Run Locally
   ```bash
      # Start Backend
         > uvicorn app:app --reload
      # Start Frontend
         > npm run dev
   ```

## API Endpoints
+ POST /match - Upload resume and get job matches
+ POST /upload - Upload and parse resume only
+ GET /docs - Interactive API documents


# 🤝 Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request
