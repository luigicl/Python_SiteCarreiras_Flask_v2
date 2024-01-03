from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from .helper_methods import normalize_searched_terms

load_dotenv()

database = "python_sitecarreiras_flask"
username = "sut2gsr6aszh2tgb8s92"
host = "aws.connect.psdb.cloud"
password = os.getenv('DB_Secrets')

db_connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8mb4"

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }})


def load_jobs_from_db():
    with engine.connect() as conn:
        jobs = []
        result = conn.execute(text("SELECT * from jobs ORDER BY title"))
        for row in result.all():
            jobs.append(row._asdict())
        return jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM jobs WHERE id = {id}"))
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0]._asdict()


def add_application_to_db(job_id, application, apply_date, job_title, uploaded_resume_id):
    chars_to_remove = ["'", '"']
    comments = str(application['comments'])
    for char in chars_to_remove:
        comments = comments.replace(char, "")
    with engine.connect() as conn:
        query = text(
            f"INSERT INTO applications (job_id, job_title, full_name, email, linkedin_url, github_url, comments,"
            f"resume_id, created_at, updated_at)"
            f"VALUES ('{job_id}', '{job_title}', '{application['full_name']}', '{application['email']}',"
            f"'{application['linkedin']}', '{application['github']}', '{comments}', '{uploaded_resume_id}', "
            f"'{apply_date}', '{apply_date}')")
        conn.execute(query)


def load_applications(email):
    with engine.connect() as conn:
        applications = []
        result = conn.execute(text(f"SELECT * FROM applications WHERE email = '{email}' ORDER BY created_at DESC"))
        for application in result.all():
            applications.append(application._asdict())
        return applications


def jobs_search(searched_terms):
    search_string = normalize_searched_terms(searched_terms)
    if search_string:
        with engine.connect() as conn:
            jobs = []
            result = conn.execute(text(search_string))
            for job in result.all():
                jobs.append(job._asdict())
            return jobs
    else:
        return []



