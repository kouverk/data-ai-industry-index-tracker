"""
DAG: Hacker News "Who Is Hiring" - Monthly Extraction

Fetches the latest "Who Is Hiring" thread from HN each month.
Runs on the 2nd of each month to catch the new thread.
"""

from datetime import datetime, timedelta
import requests
import pandas as pd
import re

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


HN_API_BASE = "https://hacker-news.firebaseio.com/v0"


def find_latest_hiring_thread(**context):
    """Find the most recent 'Who Is Hiring' thread ID."""
    # Get whoishiring's submissions
    url = f"{HN_API_BASE}/user/whoishiring.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    user_data = response.json()

    submitted = user_data.get('submitted', [])[:20]  # Check last 20 submissions

    # Find the most recent "Who is hiring" thread
    for story_id in submitted:
        story_url = f"{HN_API_BASE}/item/{story_id}.json"
        story = requests.get(story_url, timeout=10).json()

        if story and story.get('title'):
            title = story['title'].lower()
            if 'who is hiring' in title and 'freelancer' not in title:
                # Extract month/year from title like "Ask HN: Who is hiring? (January 2024)"
                match = re.search(r'\((\w+ \d{4})\)', story.get('title', ''))
                thread_month = match.group(1) if match else 'Unknown'

                context['ti'].xcom_push(key='thread_id', value=story_id)
                context['ti'].xcom_push(key='thread_month', value=thread_month)
                context['ti'].xcom_push(key='thread_title', value=story['title'])

                print(f"Found thread: {story['title']} (ID: {story_id})")
                return story_id

    raise ValueError("Could not find 'Who is hiring' thread")


def extract_job_postings(**context):
    """Extract all job postings from the hiring thread."""
    thread_id = context['ti'].xcom_pull(key='thread_id', task_ids='find_latest_thread')
    thread_month = context['ti'].xcom_pull(key='thread_month', task_ids='find_latest_thread')

    # Get the thread to find comment IDs
    thread_url = f"{HN_API_BASE}/item/{thread_id}.json"
    thread = requests.get(thread_url, timeout=30).json()

    comment_ids = thread.get('kids', [])
    print(f"Found {len(comment_ids)} top-level comments")

    job_postings = []
    for comment_id in comment_ids:
        try:
            comment_url = f"{HN_API_BASE}/item/{comment_id}.json"
            comment = requests.get(comment_url, timeout=10).json()

            if comment and not comment.get('deleted') and not comment.get('dead'):
                job_postings.append({
                    'id': str(comment_id),
                    'thread_id': str(thread_id),
                    'thread_month': thread_month,
                    'author': comment.get('by', 'unknown'),
                    'text': comment.get('text', ''),
                    'posted_at': datetime.fromtimestamp(comment.get('time', 0)).isoformat()
                })
        except Exception as e:
            print(f"Error fetching comment {comment_id}: {e}")

    context['ti'].xcom_push(key='job_postings', value=job_postings)
    print(f"Extracted {len(job_postings)} job postings")
    return len(job_postings)


def load_to_snowflake(**context):
    """Load new job postings to Snowflake."""
    job_postings = context['ti'].xcom_pull(key='job_postings', task_ids='extract_job_postings')
    thread_month = context['ti'].xcom_pull(key='thread_month', task_ids='find_latest_thread')

    if not job_postings:
        print("No job postings to load")
        return 0

    hook = SnowflakeHook(snowflake_conn_id='snowflake_default')
    conn = hook.get_conn()
    cursor = conn.cursor()

    # Check if this month already exists
    cursor.execute(
        "SELECT COUNT(*) FROM raw_hn_job_postings WHERE thread_month = %s",
        (thread_month,)
    )
    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        print(f"Thread for {thread_month} already exists ({existing_count} posts). Skipping.")
        return 0

    # Insert new postings
    inserted = 0
    for post in job_postings:
        try:
            cursor.execute("""
                INSERT INTO raw_hn_job_postings
                (id, thread_id, thread_month, author, text, posted_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                post['id'],
                post['thread_id'],
                post['thread_month'],
                post['author'],
                post['text'],
                post['posted_at']
            ))
            inserted += 1
        except Exception as e:
            print(f"Error inserting post {post['id']}: {e}")

    conn.commit()
    cursor.close()

    print(f"Loaded {inserted} new job postings for {thread_month}")
    return inserted


# DAG Definition
default_args = {
    'owner': 'data_ai_index',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
    'hn_monthly_hiring',
    default_args=default_args,
    description='Extract monthly HN Who Is Hiring job postings',
    schedule_interval='0 12 2 * *',  # 12 PM UTC on the 2nd of each month
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['hn', 'monthly', 'extraction'],
) as dag:

    find_thread = PythonOperator(
        task_id='find_latest_thread',
        python_callable=find_latest_hiring_thread,
    )

    extract_posts = PythonOperator(
        task_id='extract_job_postings',
        python_callable=extract_job_postings,
    )

    load_posts = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_to_snowflake,
    )

    find_thread >> extract_posts >> load_posts
