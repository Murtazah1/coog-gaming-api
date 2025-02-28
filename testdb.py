# test_db.py
from databases import engine, SessionLocal

def test_db_connection():
    try:
        # Attempt to connect to the database
        with engine.connect() as connection:
            print("✅ Database connection successful!")
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_db_connection()