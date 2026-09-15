import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Oracle connection: oracle+oracledb://<user>:<password>@<host>:<port>/?service_name=<service>
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "oracle+oracledb://system:system@localhost:1521/?service_name=XEPDB1"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")

    # JWT signing key + algorithm — used to issue JIT access tokens
    JWT_SECRET = os.environ.get("JWT_SECRET", "jwt-dev-secret-change-this")
    JWT_ALGORITHM = "HS256"

    # Default token validity if a visit doesn't specify (in minutes)
    DEFAULT_TOKEN_VALIDITY_MINUTES = 60