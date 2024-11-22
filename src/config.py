import os
from dotenv import load_dotenv
load_dotenv()



class Settings:
    def __init__(self) -> None:
        self.URL_Phonebook: str = os.getenv("URL_Phonebook")
        self.ROOT_DIRECTORY_OF_DOCUMENTS: str = os.getenv("ROOT_DIRECTORY_OF_DOCUMENTS")
        self.DEBUG: bool = os.getenv("DEBUG")
        self.USER: str = os.getenv("USER")
        self.PASWORD: str = os.getenv("PASWORD")
        self.PASSHASH: str = os.getenv("PASSHASH")
        
        self.DataBase_HOST: str = os.getenv("DataBase_HOST")
        self.DataBase_PORT: int = os.getenv("DataBase_PORT")
        self.DataBase_USER: str = os.getenv("DataBase_USER")
        self.DataBase_PASS: str = os.getenv("DataBase_PASS")
        self.DataBase_NAME: str = os.getenv("DataBase_NAME")
        
        # self.DATABASE_URL_ASUNC: str = f"postgresql+asyncpg://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
        # self.DATABASE_URL_SUNC: str = f"postgresql+psycopg2://{self.DataBase_USER}:{self.DataBase_PASS}@{self.DataBase_HOST}:{self.DataBase_PORT}/{self.DataBase_NAME}"
        
        self.DATABASE_URL_ASUNC: str = f"sqlite+aiosqlite:///src/db.db"
        self.DATABASE_URL_SUNC: str = f"sqlite:///src/db.db"
        
        # self.DATABASE_URL_ASUNC: str = f"sqlite+aiosqlite:///db.db"
        # self.DATABASE_URL_SUNC: str = f"sqlite:///db.db"


        
        self.REDIS_URL: str = os.getenv("REDIS_URL")
        self.TIMEZONE: str = os.getenv("TIMEZONE")
        self.BEAT_DBURL: str = os.getenv("BEAT_DBURL")
        self.BEAT_RESULT: str = os.getenv("BEAT_RESULT")
        self.FLOWER_PORT: str = os.getenv("FLOWER_PORT")
        self.ROOT_PATH: str = os.getenv("ROOT_PATH")


settings = Settings()