import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
STANDARD_USER = os.getenv("STANDARD_USER", "standard_user")
PASSWORD = os.getenv("PASSWORD", "secret123")
LOCKED_OUT_USER = os.getenv("LOCKED_OUT_USER", "locked_user")
