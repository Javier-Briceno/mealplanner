from openai import OpenAI
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.engine.base import Connection


load_dotenv()

# database credentials
user=os.getenv("PGUSER")
password=os.getenv("PGPASSWORD")
host=os.getenv("PGHOST")
port=os.getenv("PGPORT")
database=os.getenv("PGDB")

# OpenAi client configuration
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database connection configuration
def create_db_connection() -> Engine:
    try:
        engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    )
        return engine
    except Exception as e:
        print(f"Error creating database connection: {e}")
        raise
    
def get_db_connection() -> Connection:
    try:
        engine = create_db_connection()
        connection = engine.connect()
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
    
    
if __name__ == "__main__":
    # Test database connection
    conn = get_db_connection()
    if conn:
        print("Database connection successful")
        conn.close()
