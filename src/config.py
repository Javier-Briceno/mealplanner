from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
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

def init_ingredients_db() -> None:
    try:
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ingredients (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) UNIQUE NOT NULL,
                    unit VARCHAR(50) NOT NULL,
                    calories_100_g FLOAT DEFAULT 0.0,
                    protein_100_g FLOAT DEFAULT 0.0,
                    carbs_100_g FLOAT DEFAULT 0.0,
                    fat_100_g FLOAT DEFAULT 0.0
                );
            """))
            print("Ingredients table created or already exists.")
    except SQLAlchemyError as e:
        print(f"Error creating ingredients table: {e}")
        raise


if __name__ == "__main__":
    # Test database connection
    try:
        with engine.connect() as conn:
            print("Database connection successful")
    except SQLAlchemyError as e:
        print(f"Database connection failed: {e}")
        
    # Initialize ingredients database
    init_ingredients_db()
