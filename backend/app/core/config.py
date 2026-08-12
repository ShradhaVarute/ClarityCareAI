import os
from dotenv import load_dotenv

import secrets

SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")