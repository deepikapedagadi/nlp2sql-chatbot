import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()

#load db creds
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
database = os.getenv("PG_DB")

#create connection
def get_connection():
    try:
        conn = psycopg2.connect(
            host = os.getenv("PG_HOST"),
            port = os.getenv("PG_PORT"),
            user = os.getenv("PG_USER"),
            password = os.getenv("PG_PASSWORD"),
            database = os.getenv("PG_DB")
        )
        return conn
    except Exception as e:
        raise Exception(f"DB connection error -> {e}")
    
#run select queries
def  run_select_query(query, params=None):
    """Executes select queries n returns clean JSON like results"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        data = cur.fetchall()
        conn.close()
        return data
    except Exception as e:
        return {"error": str(e)}
    
#run  INSERT/UPDATE/DELETE 
def run_modify_query(query, params=None):
    """exec I/U/D, returns row_count + success message"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params)
        affected = cur.rowcount
        conn.commit()
        conn.close()
        return {"success": True, "rows_affected": affected}
    except Exception as e:
        return {"error": str(e)}