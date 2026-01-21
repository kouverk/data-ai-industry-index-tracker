"""
Load raw data from local parquet/CSV files into Snowflake.
"""

import os
import json
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_connection():
    """Create Snowflake connection."""
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

def load_hn_data():
    """Load HN job postings to Snowflake."""
    print("Loading HN data...")

    # Read parquet file
    parquet_path = os.path.join(PROJECT_ROOT, "data/raw/hn_who_is_hiring.parquet")
    df = pd.read_parquet(parquet_path)

    # Rename columns to match Snowflake table
    df = df.rename(columns={
        'by': 'author',
        'parent_id': 'thread_id'
    })

    # Select and order columns to match table schema
    df = df[['id', 'thread_id', 'thread_month', 'author', 'text', 'posted_at']]

    # Convert column names to uppercase (Snowflake convention)
    df.columns = [c.upper() for c in df.columns]

    print(f"  Records to load: {len(df):,}")

    conn = get_connection()
    cursor = conn.cursor()

    # Truncate existing data (full refresh)
    cursor.execute("TRUNCATE TABLE raw_hn_job_postings")

    # Load data using write_pandas
    success, num_chunks, num_rows, _ = write_pandas(
        conn, df, 'RAW_HN_JOB_POSTINGS',
        quote_identifiers=False
    )

    print(f"  ✓ Loaded {num_rows:,} rows to raw_hn_job_postings")

    cursor.close()
    conn.close()

def load_github_data():
    """Load GitHub repo stats to Snowflake."""
    print("Loading GitHub data...")

    # Read JSON file
    json_path = os.path.join(PROJECT_ROOT, "data/raw/github_repo_stats.json")
    with open(json_path) as f:
        data = json.load(f)

    # Flatten to DataFrame
    rows = []
    for repo in data['repos']:
        rows.append({
            'repo_name': repo['name'],
            'full_name': repo['full_name'],
            'category': repo.get('category', 'unknown'),
            'stars': repo['stars'],
            'forks': repo['forks'],
            'open_issues': repo['open_issues'],
            'watchers': repo['watchers'],
            'language': repo['language'],
            'description': repo['description'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
            'pushed_at': repo['pushed_at'],
            'fetched_at': data['fetched_at']
        })

    df = pd.DataFrame(rows)

    # Convert timestamps
    for col in ['created_at', 'updated_at', 'pushed_at', 'fetched_at']:
        df[col] = pd.to_datetime(df[col])

    # Uppercase columns
    df.columns = [c.upper() for c in df.columns]

    print(f"  Records to load: {len(df):,}")

    conn = get_connection()
    cursor = conn.cursor()

    # Truncate existing data
    cursor.execute("TRUNCATE TABLE raw_github_repo_stats")

    # Load data
    success, num_chunks, num_rows, _ = write_pandas(
        conn, df, 'RAW_GITHUB_REPO_STATS',
        quote_identifiers=False
    )

    print(f"  ✓ Loaded {num_rows:,} rows to raw_github_repo_stats")

    cursor.close()
    conn.close()

def load_linkedin_data():
    """Load LinkedIn job data to Snowflake."""
    print("Loading LinkedIn data...")

    linkedin_dir = os.path.join(PROJECT_ROOT, "data/raw/linkedin")

    conn = get_connection()
    cursor = conn.cursor()

    # Load job postings
    postings_path = os.path.join(linkedin_dir, "linkedin_job_postings.csv")
    if os.path.exists(postings_path):
        print("  Loading job postings...")
        df = pd.read_csv(postings_path, low_memory=False)

        # Select columns that match our table
        columns_map = {
            'job_link': 'job_link',
            'last_processed_time': 'last_processed_time',
            'got_summary': 'got_summary',
            'got_ner': 'got_ner',
            'is_being_worked': 'is_being_worked',
            'job_title': 'job_title',
            'company': 'company',
            'job_location': 'job_location',
            'first_seen': 'first_seen',
            'search_city': 'search_city',
            'search_country': 'search_country',
            'search_position': 'search_position',
            'job_level': 'job_level',
            'job_type': 'job_type'
        }

        # Only keep columns that exist in the CSV
        available_cols = [c for c in columns_map.keys() if c in df.columns]
        df = df[available_cols]

        # Convert timestamps if present
        for col in ['last_processed_time', 'first_seen']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        df.columns = [c.upper() for c in df.columns]

        print(f"    Records: {len(df):,}")

        cursor.execute("TRUNCATE TABLE raw_linkedin_postings")
        success, num_chunks, num_rows, _ = write_pandas(
            conn, df, 'RAW_LINKEDIN_POSTINGS',
            quote_identifiers=False
        )
        print(f"    ✓ Loaded {num_rows:,} rows to raw_linkedin_postings")
    else:
        print(f"  ✗ Job postings file not found: {postings_path}")

    # Load skills
    skills_path = os.path.join(linkedin_dir, "job_skills.csv")
    if os.path.exists(skills_path):
        print("  Loading skills...")
        df = pd.read_csv(skills_path, low_memory=False)
        df.columns = [c.upper() for c in df.columns]

        print(f"    Records: {len(df):,}")

        cursor.execute("TRUNCATE TABLE raw_linkedin_skills")
        success, num_chunks, num_rows, _ = write_pandas(
            conn, df, 'RAW_LINKEDIN_SKILLS',
            quote_identifiers=False
        )
        print(f"    ✓ Loaded {num_rows:,} rows to raw_linkedin_skills")
    else:
        print(f"  ✗ Skills file not found: {skills_path}")

    # Load summaries
    summary_path = os.path.join(linkedin_dir, "job_summary.csv")
    if os.path.exists(summary_path):
        print("  Loading summaries...")
        df = pd.read_csv(summary_path, low_memory=False)
        df.columns = [c.upper() for c in df.columns]

        print(f"    Records: {len(df):,}")

        cursor.execute("TRUNCATE TABLE raw_linkedin_summaries")
        success, num_chunks, num_rows, _ = write_pandas(
            conn, df, 'RAW_LINKEDIN_SUMMARIES',
            quote_identifiers=False
        )
        print(f"    ✓ Loaded {num_rows:,} rows to raw_linkedin_summaries")
    else:
        print(f"  ✗ Summary file not found: {summary_path}")

    cursor.close()
    conn.close()

def verify_loads():
    """Verify data was loaded correctly."""
    print("\nVerifying loads...")

    conn = get_connection()
    cursor = conn.cursor()

    tables = [
        'raw_hn_job_postings',
        'raw_github_repo_stats',
        'raw_linkedin_postings',
        'raw_linkedin_skills',
        'raw_linkedin_summaries'
    ]

    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count:,} rows")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        source = sys.argv[1]
        if source == "hn":
            load_hn_data()
        elif source == "github":
            load_github_data()
        elif source == "linkedin":
            load_linkedin_data()
        elif source == "verify":
            verify_loads()
        else:
            print(f"Unknown source: {source}")
            print("Usage: python load_data.py [hn|github|linkedin|verify]")
    else:
        # Load all
        load_hn_data()
        load_github_data()
        load_linkedin_data()
        verify_loads()
