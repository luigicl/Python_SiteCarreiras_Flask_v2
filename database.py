import sqlalchemy
from sqlalchemy import create_engine, text
import os

database = "python_sitecarreiras_flask"
username = "no0m6cfwb9kl71wtj5no"
host = "aws.connect.psdb.cloud"
password = os.environ['DB_Secret']

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
        result = conn.execute(text("SELECT * from jobs"))
        for row in result.all():
            jobs.append(row._asdict())
        return jobs










