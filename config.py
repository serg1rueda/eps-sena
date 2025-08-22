import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://neondb_owner:npg_vw2YZckmCDp6@ep-bold-rice-ad6yxmbi-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secretito123")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secretito_123")  # importante definir en Render
    SWAGGER = {
        "title": "EPS-SENA API",
        "uiversion": 3
    }
