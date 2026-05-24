import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    RECIPIENTS_RAW = os.getenv("RECIPIENTS", "")
    
    @property
    def RECIPIENTS(self):
        return [
            email.strip()
            for email in self.RECIPIENTS_RAW.split(",")
            if email.strip()
        ]


settings = Settings()