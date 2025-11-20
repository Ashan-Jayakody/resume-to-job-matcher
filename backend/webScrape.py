import requests
from bs4 import BeautifulSoup
import psycopg2
from getDbConnection import get_db_connection

# Function for scrape jobs from web
def jobs_scrape_and_update():

    urls = [
        "https://jobber.lk/",
        "https://jobber.lk/vacancies/accounting-auditing-jobs-in-sri-lanka",
        "https://jobber.lk/vacancies/banking-and-financial-services-jobs-in-sri-lanka",
        "https://jobber.lk/vacancies/it-software-internet-jobs-in-sri-lanka",
    ]

    all_jobs = []

    for url in urls:
        print(f"\nScraping: {url}\n")

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch URL {url}: {e}")
            continue  # continue next URL

        try:
            soup = BeautifulSoup(response.content, "html.parser")
            jobCard = soup.select('a > div.job_item')
            print(f"Found job cards on page: {len(jobCard)}")

            for job in jobCard:
                title_tag = job.find("h3", class_="title")
                title = title_tag.get_text(strip=True)

                parent_a = job.find_parent("a")
                link = parent_a["href"]

                desc_tag = job.select_one("div.description")
                description = desc_tag.get_text(strip=True) if desc_tag else None

                company_tag = job.find("p", class_="list_company")
                company = company_tag.get_text(strip=True) if company_tag else None

                location_tag = job.find("p", class_="location")
                location = location_tag.get_text(strip=True) if location_tag else None

                all_jobs.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "company": company,
                    "location": location
                })

        except Exception as e:
            print(f"Error parsing HTML for {url}: {e}")
            continue

    print(f"\nTotal jobs scraped from all URLs: {len(all_jobs)}\n")

    # Save to DB
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        for job in all_jobs:
            try:
                cur.execute("""
                    INSERT INTO jobs (title, link, description, company, location)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO UPDATE
                    SET title = EXCLUDED.title,
                        description = EXCLUDED.description,
                        company = EXCLUDED.company,
                        location = EXCLUDED.location
                """, (
                    job['title'],
                    job['link'],
                    job['description'],
                    job['company'],
                    job['location']
                ))

            except Exception as e:
                print("Insert failed:", e)
                conn.rollback()
            else:
                conn.commit()

        print("Database update: SUCCESS")

    except psycopg2.Error as e:
        print("DB error:", e)

    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

jobs_scrape_and_update()