import os

from dotenv import load_dotenv

load_dotenv()

DBIP = os.getenv('DBIP')
PGUSER = str(os.getenv('DBUSER'))
PGPASS = str(os.getenv('DBPASSWORD'))
DB = str(os.getenv('NAMEDB'))

DBIP_TEST = os.getenv('DBIP_TEST')
PGUSER_TEST = str(os.getenv('DBUSER_TEST'))
PGPASS_TEST = str(os.getenv('DBPASSWORD_TEST'))
DB_TEST = str(os.getenv('NAMEDB_TEST'))

POSTGRES_URI = f'postgresql+asyncpg://{PGUSER}:{PGPASS}@{DBIP}/{DB}'
POSTGRES_URI_TEST = f'postgresql+asyncpg://{PGUSER_TEST}:{PGPASS_TEST}@{DBIP_TEST}/{DB_TEST}'

SECRET_KEY = str(os.getenv('SECRET_KEY'))
ALGORITHM = str(os.getenv('ALGORITHM'))
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES'))

REDIS_SERVER: str = os.getenv("REDIS_SERVER")
REDIS_PORT: int = int(os.getenv("REDIS_PORT"))

SMTP_USER: str = os.getenv("SMTP_USER")
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465
