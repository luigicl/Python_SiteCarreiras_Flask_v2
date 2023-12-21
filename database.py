import sqlalchemy
from sqlalchemy import create_engine

database = "python_sitecarreiras_flask"
username = "0sw87txesopu60wgrqf6"
host = "aws.connect.psdb.cloud"
password = "pscale_pw_e43NgZUO9oi5P2bGZ2aXFW1oEsFlBazvB6k0tQ3OIpB"

db_connection_string = f"mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8mb4"

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }})











