from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv()

# database credentials
user=os.getenv("PGUSER")
password=os.getenv("PGPASSWORD")
host=os.getenv("PGHOST")
port=os.getenv("PGPORT")
database=os.getenv("PGDB")

# OpenAI client configuration
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database connection configuration
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)

if __name__ == "__main__":
    # Test database connection
    try:
        with engine.connect() as conn:
            print("Database connection successful")
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
