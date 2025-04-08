import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def init_database():
    """Initialize the database and create necessary tables."""
    conn = None
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Create database if it doesn't exist
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_CONFIG['dbname'],))
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_CONFIG['dbname'])))
            print(f"Database {DB_CONFIG['dbname']} created successfully.")
        
        cur.close()
        conn.close()
        
        # Connect to the new database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Create games table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id SERIAL PRIMARY KEY,
            game_date DATE NOT NULL,
            team1_score INTEGER NOT NULL,
            team2_score INTEGER NOT NULL,
            game_data JSONB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Create player_stats table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS player_stats (
            id SERIAL PRIMARY KEY,
            player_name VARCHAR(100) UNIQUE NOT NULL,
            good_serves INTEGER DEFAULT 0,
            bad_serves INTEGER DEFAULT 0,
            successful_sets INTEGER DEFAULT 0,
            failed_sets INTEGER DEFAULT 0,
            successful_hits INTEGER DEFAULT 0,
            failed_hits INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        conn.commit()
        print("Tables created successfully.")
        
    except psycopg2.Error as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    init_database() 