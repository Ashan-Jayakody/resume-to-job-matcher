import requests
from bs4 import BeautifulSoup
import psycopg2
from getDbConnection import get_db_connection

# Function for scrape jobs from web
def jobs_scrape_and_update():
    
    url = "https://jobber.lk/vacancies/it-software-internet-jobs-in-sri-lanka"
    

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch jobs: {e}")
        return

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        jobCard = soup.select('a> div.job_item')
        print("Found job cards:", len(jobCard))
        jobs=[]

        for job in jobCard:
            title_tag = job.find("h3", class_="title")
            title = title_tag.get_text(strip=True)
        
            parent_a = job.find_parent("a")
            link = parent_a["href"]

            desc_tag = job.select_one("div", class_ ="description")
            description = desc_tag.get_text(strip=True) if desc_tag else None
        
            company_tag = job.find("p", class_="list_company")
            company = company_tag.get_text(strip=True)

            location_tag = job.find("p", class_= "location")
            location = location_tag.get_text(strip=True)

            jobs.append(
                {
                    "title": title,
                    "link": link,
                    "description": description,
                    "company": company,
                    "location": location
                }
            )
    except Exception as e:
        print(f"Error parsing: {e}")
        return


# Save the data to PostgreSQL DB

    try:
        #connection to theDB
        conn = get_db_connection()
        cur = conn.cursor()

        for job in jobs:
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
                    job['title'], job['link'], job['description'], job['company'], job['location']
                ))
            except Exception as e:
                print(f"Error inserting to the table: {e}")
                conn.rollback() #undo the failed insert
            else:
                conn.commit()
        print(f"Updated success")
    except psycopg2.Error as e:
        print(f"Database or querry error: {e}")
    
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

jobs_scrape_and_update()