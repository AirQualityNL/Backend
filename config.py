from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
