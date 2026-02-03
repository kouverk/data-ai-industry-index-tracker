"""
LLM-Powered Skill Extraction

Uses Claude to extract skills/technologies from job posting text.
Runs on a sample of posts to demonstrate AI-in-the-pipeline capability,
while regex handles the full dataset for cost efficiency.
"""

import os
import json
import time
import hashlib
from datetime import datetime
from dotenv import load_dotenv
import anthropic
import snowflake.connector
import pandas as pd
from tqdm import tqdm

load_dotenv('.env')

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Snowflake connection
def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

# Extraction prompt (without job text - will be appended)
EXTRACTION_PROMPT_PREFIX = """You are a data engineering expert. Extract all technologies, tools, frameworks, languages, and platforms mentioned in this job posting.

Return a JSON object with this exact structure:
{"technologies": [{"name": "canonical_name", "category": "category", "confidence": 0.0-1.0}], "roles": [{"name": "role_title", "tier": "core|adjacent|emerging", "confidence": 0.0-1.0}]}

Categories for technologies:
- orchestration (Airflow, Dagster, Prefect)
- transformation (dbt, Spark, pandas)
- warehouse (Snowflake, BigQuery, Redshift)
- streaming (Kafka, Flink, Kinesis)
- language (Python, SQL, Scala)
- cloud (AWS, GCP, Azure)
- ml_framework (PyTorch, TensorFlow)
- llm (OpenAI, LangChain, Claude)
- infrastructure (Kubernetes, Docker, Terraform)
- bi (Tableau, Looker, Metabase)
- database (PostgreSQL, MySQL, MongoDB)
- etl_elt (Fivetran, Airbyte)
- vector_db (Pinecone, Chroma)
- mlops (MLflow, Kubeflow)
- other

Role tiers:
- core: Data Engineer, Analytics Engineer, Data Scientist, Data Analyst
- adjacent: ML Engineer, Platform Engineer, Backend Engineer
- emerging: AI Engineer, MLOps Engineer, LLM Engineer

Only include items explicitly mentioned. Use canonical names (e.g., "Kubernetes" not "k8s", "PostgreSQL" not "postgres").

Job posting:
"""

EXTRACTION_PROMPT_SUFFIX = """

Return ONLY the JSON object, no other text."""


def extract_skills_with_llm(job_text: str, posting_id: str) -> dict:
    """Extract skills from a single job posting using Claude."""
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": EXTRACTION_PROMPT_PREFIX + job_text[:4000] + EXTRACTION_PROMPT_SUFFIX
                }
            ]
        )

        # Parse response
        content = response.content[0].text.strip()

        # Handle potential markdown code blocks
        if "```" in content:
            # Extract content between code fences
            parts = content.split("```")
            if len(parts) >= 2:
                content = parts[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()

        # Find the JSON object - look for opening brace
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        if start_idx == -1 or end_idx == -1:
            raise json.JSONDecodeError("No JSON object found", content, 0)
        content = content[start_idx:end_idx+1]

        result = json.loads(content)
        result['posting_id'] = posting_id
        result['extraction_method'] = 'llm'
        result['model'] = 'claude-3-haiku-20240307'
        result['extracted_at'] = datetime.utcnow().isoformat()

        return result

    except json.JSONDecodeError as e:
        print(f"JSON parse error for {posting_id}: {e}")
        return {
            'posting_id': posting_id,
            'technologies': [],
            'roles': [],
            'extraction_method': 'llm',
            'error': str(e)
        }
    except Exception as e:
        print(f"Error extracting {posting_id}: {e}")
        return {
            'posting_id': posting_id,
            'technologies': [],
            'roles': [],
            'extraction_method': 'llm',
            'error': str(e)
        }


def load_sample_posts(limit: int = 10000) -> pd.DataFrame:
    """Load a random sample of job postings from Snowflake."""
    conn = get_snowflake_connection()

    query = f"""
    SELECT
        posting_id,
        posting_text,
        posting_month,
        posting_year
    FROM KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
    WHERE posting_text IS NOT NULL
        AND LENGTH(posting_text) > 100
    ORDER BY RANDOM()
    LIMIT {limit}
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


def save_results_to_snowflake(results: list):
    """Save extraction results to Snowflake."""
    conn = get_snowflake_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS KOUVERK_DATA_INDUSTRY.raw_llm_skill_extractions (
        posting_id VARCHAR,
        technologies VARIANT,
        roles VARIANT,
        extraction_method VARCHAR,
        model VARCHAR,
        extracted_at TIMESTAMP,
        error VARCHAR
    )
    """)

    # Insert results using SELECT to allow PARSE_JSON
    for result in results:
        tech_json = json.dumps(result.get('technologies', [])).replace("'", "''")
        roles_json = json.dumps(result.get('roles', [])).replace("'", "''")
        error_val = result.get('error')
        error_str = f"'{error_val.replace(chr(39), chr(39)+chr(39))}'" if error_val else 'NULL'

        cur.execute(f"""
        INSERT INTO KOUVERK_DATA_INDUSTRY.raw_llm_skill_extractions
        (posting_id, technologies, roles, extraction_method, model, extracted_at, error)
        SELECT
            %s,
            PARSE_JSON('{tech_json}'),
            PARSE_JSON('{roles_json}'),
            %s,
            %s,
            %s,
            {error_str}
        """, (
            result.get('posting_id'),
            result.get('extraction_method'),
            result.get('model'),
            result.get('extracted_at')
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Saved {len(results)} results to Snowflake")


def run_extraction(sample_size: int = 10000, batch_size: int = 100):
    """Run the full extraction pipeline."""
    print(f"Loading {sample_size} sample posts...")
    df = load_sample_posts(sample_size)
    print(f"Loaded {len(df)} posts")

    results = []
    errors = 0

    print("Starting extraction...")
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        result = extract_skills_with_llm(row['POSTING_TEXT'], str(row['POSTING_ID']))
        results.append(result)

        if result.get('error'):
            errors += 1

        # Save in batches
        if len(results) >= batch_size:
            save_results_to_snowflake(results)
            results = []

        # Rate limiting - be nice to the API
        time.sleep(0.1)

    # Save remaining results
    if results:
        save_results_to_snowflake(results)

    print(f"\nExtraction complete!")
    print(f"Total processed: {len(df)}")
    print(f"Errors: {errors}")


def estimate_cost(sample_size: int = 10000):
    """Estimate the cost of running extraction."""
    # Haiku pricing: $0.25/M input, $1.25/M output
    avg_input_tokens = 800  # ~job posting + prompt
    avg_output_tokens = 200  # JSON response

    total_input = sample_size * avg_input_tokens / 1_000_000
    total_output = sample_size * avg_output_tokens / 1_000_000

    cost = (total_input * 0.25) + (total_output * 1.25)

    print(f"Estimated cost for {sample_size:,} posts:")
    print(f"  Input tokens: {sample_size * avg_input_tokens:,} (~${total_input * 0.25:.2f})")
    print(f"  Output tokens: {sample_size * avg_output_tokens:,} (~${total_output * 1.25:.2f})")
    print(f"  Total: ~${cost:.2f}")
    return cost


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM Skill Extraction")
    parser.add_argument("--sample-size", type=int, default=10000, help="Number of posts to process")
    parser.add_argument("--estimate-only", action="store_true", help="Only estimate cost, don't run")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size for saving to Snowflake")

    args = parser.parse_args()

    if args.estimate_only:
        estimate_cost(args.sample_size)
    else:
        print("Cost estimate:")
        estimate_cost(args.sample_size)
        print("\nStarting extraction in 5 seconds... (Ctrl+C to cancel)")
        time.sleep(5)
        run_extraction(args.sample_size, args.batch_size)
