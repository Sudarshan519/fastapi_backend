import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME:str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    MySQL_USER : str = os.getenv("MYSQL_USER")
    MySQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MySQL_SERVER : str = os.getenv("MySQL_SERVER","localhost")
    MySQL_PORT : str = os.getenv("MySQL_PORT",3306) # default MySQL port is 5432
    MySQL_DB : str = os.getenv("MYSQL_DB")
    DATABASE_URL = f"mysql+mysqlconnector://{MySQL_USER}:{MySQL_PASSWORD}@{MySQL_SERVER}:{MySQL_PORT}/{MySQL_DB}"
    SECRET_KEY :str = os.getenv("SECRET_KEY")   #new
    ALGORITHM = "HS256"                         #new
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  #in mins  #new
    TEST_USER_EMAIL = "test@example.com"  #new
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL","redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND","redis://127.0.0.1:6379/0")

settings = Settings()