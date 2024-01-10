from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from .helper_methods import normalize_searched_terms
from carreiras_python.gdrive_api_methods import GoogleDriveService

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


def load_applications_from_db():
    with engine.connect() as conn:
        applications = []
        result = conn.execute(text("SELECT * from applications ORDER BY job_title, full_name, created_at"))
        for row in result.all():
            applications.append(row._asdict())
        return applications


def load_my_applications(email):
    with engine.connect() as conn:
        applications = []
        result = conn.execute(text(f"SELECT * FROM applications WHERE email = '{email}' ORDER BY created_at DESC"))
        for application in result.all():
            applications.append(application._asdict())
        return applications


def load_application_by_id(id):
    with engine.connect() as conn:
        query = text(
            f"SELECT * FROM applications WHERE id = :id"
            )
        result = conn.execute(query, {
                    'id': id,
                    })
        applications = []
        for application in result.all():
            applications.append(application._asdict())
        return applications


def add_application_to_db(job_id, application, apply_date, job_title, uploaded_resume_id):
    with engine.connect() as conn:
        query = text(
            f"INSERT INTO applications (job_id, job_title, full_name, email, linkedin_url, github_url, comments,"
            f"resume_id, created_at, updated_at)"
            f"VALUES (:job_id, :job_title, :full_name, :email, :linkedin_url, :github_url, :comments,"
            f":resume_id, :created_at, :updated_at)")
        conn.execute(query, {
                    'job_id': job_id,
                    'job_title': job_title,
                    'full_name': application.full_name.data,
                    'email': application.email.data,
                    'linkedin_url': application.linkedin.data,
                    'github_url': application.github.data,
                    'comments': application.comments.data,
                    'resume_id': uploaded_resume_id,
                    'created_at': apply_date,
                    'updated_at': apply_date
                    })


def add_new_job_to_db(formCreateJob, create_date):
    with engine.connect() as conn:
        query = text(
            f"INSERT INTO jobs (title, location, salary, currency, responsabilities, requirements,"
            f"created_at, updated_at) "
            f"VALUES (:title, :location, :salary, :currency, :responsabilities, :requirements, :created_at, "
            f":updated_at)")
        conn.execute(query, {
                    'title': formCreateJob.job_title.data,
                    'location': formCreateJob.location.data,
                    'salary': formCreateJob.salary.data,
                    'currency': formCreateJob.currency.data,
                    'responsabilities': formCreateJob.responsabilities.data,
                    'requirements': formCreateJob.requirements.data,
                    'created_at': create_date,
                    'updated_at': create_date
                    })


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


def delete_a_job(job_id):
    with engine.connect() as conn:
        query = text(
            f"DELETE FROM jobs WHERE id = :id"
            )
        conn.execute(query, {
                    'id': job_id,
                    })


def delete_a_application(application_id, resume_id):
    if resume_id:
        GoogleDriveService().delete_file(resume_id)
    with engine.connect() as conn:
        query = text(
            f"DELETE FROM applications WHERE id = :id"
            )
        conn.execute(query, {
                    'id': application_id,
                    })
