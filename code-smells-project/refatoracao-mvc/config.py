import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-fallback")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///loja.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
