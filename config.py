import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/eps_sena"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secretito123")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_secretito_123")  # importante definir en Render
    SWAGGER = {
        "title": "EPS-SENA API",
        "uiversion": 3
    }
