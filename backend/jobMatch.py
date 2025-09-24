import psycopg2
from pathlib import Path

# Skills list to check
skill_keywords = [
    "python", "java", "sql", "react", "javascript", "css",
    "django", "html", "c++", "node", "express", "mongodb"
]

def extract_skills(text: str):
    text_to_lower = text.lower()
    found = []
    for skill in skill_keywords:
        if skill in text_to_lower:
            found.append(skill)
    return list(set(found))

def match_jobs(user_skills: list):
    try:
        conn = psycopg2.connect("dbname=jobs user=postgres password=admin123")
        cur = conn.cursor()
        cur.execute("SELECT title, link, description, company, location FROM jobs")
        jobs_list = cur.fetchall()
    except psycopg2.Error as e:
        print(f"Error fetch from table: {e}")
    finally:
        cur.close()
        conn.close()

    result = []
    for job in jobs_list:
        title, link, description, company, location = job

        desc_lower = description.lower() if description else ""
        
        #extract skills  from job description
        job_skills = [skill for skill in skill_keywords if skill in desc_lower]

        matching_skills = list(set(user_skills) & set(job_skills))
        overlap = len(matching_skills)

        if overlap > 0:
            result.append({
                "title": title,
                "link": link,
                "skills_required": job_skills,
                "matching_skills": matching_skills,
                "score": overlap,
                "company": company,
                "location": location
        })
    #sort list by decending order
    return sorted(result, key=lambda x: x["score"], reverse=True)