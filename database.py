import sqlalchemy
from sqlalchemy import create_engine

database = "python_sitecarreiras_flask"
username = "no0m6cfwb9kl71wtj5no"
host = "aws.connect.psdb.cloud"
password = "pscale_pw_b7A9Lw3EBU1wox9alzcJSv3pSg0Zu2yNIy0WNIQ5mf9"

db_connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8mb4"

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }})












