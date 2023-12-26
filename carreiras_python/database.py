import sqlalchemy
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

database = "python_sitecarreiras_flask"
username = "no0m6cfwb9kl71wtj5no"
host = "aws.connect.psdb.cloud"
password = os.environ.get('DB_Secret')

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


def add_application_to_db(job_id, application, apply_date):
    chars_to_remove = ["'", '"']
    comments = str(application['comments'])
    for char in chars_to_remove:
        comments = comments.replace(char, "")
    with engine.connect() as conn:
        query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, github_url, comments, "
                     "created_at, updated_at) VALUES (:job_id, :full_name, :email, :linkedin_url, :github_url, "
                     ":comments, :created_at, :updated_at)")
        query = text(
            f"INSERT INTO applications (job_id, full_name, email, linkedin_url, github_url, comments,"
            f"created_at, updated_at)"
            f"VALUES ('{job_id}', '{application['full_name']}', '{application['email']}', '{application['linkedin']}',"
            f"'{application['github']}', '{comments}', '{apply_date}', '{apply_date}')")
        conn.execute(query)









