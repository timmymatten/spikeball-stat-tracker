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

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """
    Execute a SQL query.
    
    :param query: The SQL query to execute.
    :param params: Parameters for the query (optional).
    :param fetch: Whether to fetch results (for SELECT queries).
    :return: Fetched results if fetch=True, otherwise None.
    """
    conn = get_db_connection()
    if conn is None:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                result = cur.fetchall()
                return result
            conn.commit()
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def fetch_games():
    """Fetch all games from the database."""
    query = "SELECT * FROM games;"
    result = execute_query(query, fetch=True)
    return result if result else []  # Return an empty list if result is None

def fetch_player_stats():
    """Fetch all player stats from the database."""
    query = "SELECT * FROM player_stats;"
    result = execute_query(query, fetch=True)
    return result if result else [] # Return an empty list if result is None

def save_game(game_date, team1_score, team2_score, game_data):
    """Save a game to the database."""
    query = """
    INSERT INTO games (game_date, team1_score, team2_score, game_data)
    VALUES (%s, %s, %s, %s);
    """
    params = (game_date, team1_score, team2_score, game_data)
    execute_query(query, params)

def save_player_stats(player_name, good_serves, bad_serves, successful_sets, failed_sets, successful_hits, failed_hits):
    """Save player stats to the database."""
    query = """
    INSERT INTO player_stats (player_name, good_serves, bad_serves, successful_sets, failed_sets, successful_hits, failed_hits)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    params = (player_name, good_serves, bad_serves, successful_sets, failed_sets, successful_hits, failed_hits)
    execute_query(query, params)

def update_player_stats(player_name, good_serves, bad_serves, successful_sets, failed_sets, successful_hits, failed_hits):
    """Update player stats in the database."""
    query = """
    UPDATE player_stats
    SET good_serves = %s, bad_serves = %s, successful_sets = %s, failed_sets = %s, successful_hits = %s, failed_hits = %s
    WHERE player_name = %s;
    """
    params = (good_serves, bad_serves, successful_sets, failed_sets, successful_hits, failed_hits, player_name)
    execute_query(query, params)

def delete_game(game_id):
    """Delete a game from the database."""
    query = "DELETE FROM games WHERE id = %s;"
    params = (game_id,)
    execute_query(query, params)

def delete_player_stats(player_name):
    """Delete player stats from the database."""
    query = "DELETE FROM player_stats WHERE player_name = %s;"
    params = (player_name,)
    execute_query(query, params)