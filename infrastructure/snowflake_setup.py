"""
Snowflake setup script for Data & AI Industry Index project.
Creates schemas and tables for raw data landing.
"""

import os
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    """Create Snowflake connection from environment variables."""
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

def run_setup():
    """Set up Snowflake schemas and tables."""
    conn = get_connection()
    cursor = conn.cursor()

    schema = os.getenv('SNOWFLAKE_SCHEMA')

    print(f"Connected to Snowflake. Setting up schema: {schema}")

    # Create schema if it doesn't exist
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    cursor.execute(f"USE SCHEMA {schema}")

    # =========================================
    # RAW TABLES
    # =========================================

    # HN Who Is Hiring - raw job postings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_hn_job_postings (
            id VARCHAR,
            thread_id VARCHAR,
            thread_month VARCHAR,
            author VARCHAR,
            text TEXT,
            posted_at TIMESTAMP_NTZ,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✓ Created raw_hn_job_postings")

    # LinkedIn job postings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_linkedin_postings (
            job_link VARCHAR,
            last_processed_time TIMESTAMP_NTZ,
            got_summary VARCHAR,
            got_ner VARCHAR,
            is_being_worked VARCHAR,
            job_title VARCHAR,
            company VARCHAR,
            job_location VARCHAR,
            first_seen TIMESTAMP_NTZ,
            search_city VARCHAR,
            search_country VARCHAR,
            search_position VARCHAR,
            job_level VARCHAR,
            job_type VARCHAR,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✓ Created raw_linkedin_postings")

    # LinkedIn skills (pre-extracted from Kaggle dataset)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_linkedin_skills (
            job_link VARCHAR,
            job_skills TEXT,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✓ Created raw_linkedin_skills")

    # LinkedIn job summaries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_linkedin_summaries (
            job_link VARCHAR,
            job_summary TEXT,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✓ Created raw_linkedin_summaries")

    # GitHub repo stats (daily refresh)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_github_repo_stats (
            repo_name VARCHAR,
            full_name VARCHAR,
            category VARCHAR,
            stars INTEGER,
            forks INTEGER,
            open_issues INTEGER,
            watchers INTEGER,
            language VARCHAR,
            description TEXT,
            created_at TIMESTAMP_NTZ,
            updated_at TIMESTAMP_NTZ,
            pushed_at TIMESTAMP_NTZ,
            fetched_at TIMESTAMP_NTZ,
            _loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
    """)
    print("✓ Created raw_github_repo_stats")

    # =========================================
    # SUMMARY
    # =========================================

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = UPPER(%s)
        ORDER BY table_name
    """, (schema,))

    tables = cursor.fetchall()
    print(f"\n✓ Setup complete. Tables in {schema}:")
    for table in tables:
        print(f"  - {table[0]}")

    cursor.close()
    conn.close()

def test_connection():
    """Test Snowflake connection."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_USER(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA()")
        result = cursor.fetchone()
        print(f"✓ Connected to Snowflake")
        print(f"  User: {result[0]}")
        print(f"  Warehouse: {result[1]}")
        print(f"  Database: {result[2]}")
        print(f"  Schema: {result[3]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_connection()
    else:
        if test_connection():
            print("\n--- Running setup ---\n")
            run_setup()
