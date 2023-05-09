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

settings = Settings()