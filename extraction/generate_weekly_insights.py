"""
Automated Weekly Insights Generator

Uses Claude to analyze trend data and produce a written summary.
Designed to run as an Airflow task on a weekly schedule.
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import anthropic
import snowflake.connector
import pandas as pd

load_dotenv()

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))


def get_snowflake_connection():
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )


def get_technology_trends() -> pd.DataFrame:
    """Get recent technology trend data."""
    conn = get_snowflake_connection()

    query = """
    WITH recent AS (
        SELECT
            technology_name,
            category,
            posting_month,
            mention_count,
            total_postings,
            mention_pct
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
        WHERE posting_month >= DATEADD(month, -24, CURRENT_DATE())
    ),
    with_yoy AS (
        SELECT
            r1.technology_name,
            r1.category,
            r1.posting_month,
            r1.mention_count as current_mentions,
            r1.mention_pct as current_pct,
            r2.mention_count as prev_year_mentions,
            r2.mention_pct as prev_year_pct,
            CASE
                WHEN r2.mention_count > 0
                THEN ROUND((r1.mention_count - r2.mention_count) * 100.0 / r2.mention_count, 1)
                ELSE NULL
            END as yoy_change_pct
        FROM recent r1
        LEFT JOIN recent r2
            ON r1.technology_name = r2.technology_name
            AND r1.posting_month = DATEADD(month, 12, r2.posting_month)
        WHERE r1.posting_month = (SELECT MAX(posting_month) FROM recent)
    )
    SELECT * FROM with_yoy
    ORDER BY current_mentions DESC
    LIMIT 50
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_role_trends() -> pd.DataFrame:
    """Get recent role trend data."""
    conn = get_snowflake_connection()

    query = """
    WITH recent AS (
        SELECT
            role_name,
            tier,
            posting_month,
            mention_count,
            mention_pct
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends
        WHERE posting_month >= DATEADD(month, -24, CURRENT_DATE())
    ),
    with_yoy AS (
        SELECT
            r1.role_name,
            r1.tier,
            r1.posting_month,
            r1.mention_count as current_mentions,
            r1.mention_pct as current_pct,
            r2.mention_count as prev_year_mentions,
            CASE
                WHEN r2.mention_count > 0
                THEN ROUND((r1.mention_count - r2.mention_count) * 100.0 / r2.mention_count, 1)
                ELSE NULL
            END as yoy_change_pct
        FROM recent r1
        LEFT JOIN recent r2
            ON r1.role_name = r2.role_name
            AND r1.posting_month = DATEADD(month, 12, r2.posting_month)
        WHERE r1.posting_month = (SELECT MAX(posting_month) FROM recent)
    )
    SELECT * FROM with_yoy
    ORDER BY current_mentions DESC
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_github_highlights() -> pd.DataFrame:
    """Get GitHub repo highlights."""
    conn = get_snowflake_connection()

    query = """
    SELECT
        repo_name,
        category,
        stars,
        forks,
        activity_level,
        days_since_last_push
    FROM KOUVERK_DATA_INDUSTRY_marts.fct_github_repo_stats
    ORDER BY stars DESC
    LIMIT 20
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


def generate_insights(tech_df: pd.DataFrame, role_df: pd.DataFrame, github_df: pd.DataFrame) -> str:
    """Generate insights using Claude."""

    # Prepare data summaries
    top_growing = tech_df[tech_df['YOY_CHANGE_PCT'].notna()].nlargest(10, 'YOY_CHANGE_PCT')
    top_declining = tech_df[tech_df['YOY_CHANGE_PCT'].notna()].nsmallest(5, 'YOY_CHANGE_PCT')
    top_mentioned = tech_df.nlargest(10, 'CURRENT_MENTIONS')

    prompt = f"""You are a data/AI industry analyst. Based on the following job market and GitHub data, write a concise weekly insights report.

## Technology Trends (from HN "Who Is Hiring" job postings)

### Top 10 Most Mentioned Technologies (Latest Month)
{top_mentioned[['TECHNOLOGY_NAME', 'CATEGORY', 'CURRENT_MENTIONS', 'YOY_CHANGE_PCT']].to_string(index=False)}

### Fastest Growing Technologies (Year-over-Year)
{top_growing[['TECHNOLOGY_NAME', 'CATEGORY', 'CURRENT_MENTIONS', 'YOY_CHANGE_PCT']].to_string(index=False)}

### Declining Technologies
{top_declining[['TECHNOLOGY_NAME', 'CATEGORY', 'CURRENT_MENTIONS', 'YOY_CHANGE_PCT']].to_string(index=False)}

## Role Trends
{role_df[['ROLE_NAME', 'TIER', 'CURRENT_MENTIONS', 'YOY_CHANGE_PCT']].to_string(index=False)}

## GitHub Repository Activity
{github_df[['REPO_NAME', 'CATEGORY', 'STARS', 'ACTIVITY_LEVEL']].to_string(index=False)}

---

Write a report with these sections:
1. **Executive Summary** (2-3 sentences on the biggest trends)
2. **Technology Highlights** (3-4 bullet points on notable technology trends)
3. **Role Market** (2-3 bullet points on hiring patterns)
4. **Open Source Activity** (2-3 bullet points on GitHub trends)
5. **What to Watch** (2-3 emerging technologies or shifts to monitor)

Be specific with numbers. Mention actual percentages and technology names. Keep it under 500 words.
Format in markdown."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text


def save_insights(insights: str, output_dir: str = "docs"):
    """Save insights to a markdown file."""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"{output_dir}/WEEKLY_INSIGHTS_{timestamp}.md"

    header = f"""# Weekly Data/AI Industry Insights

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
**Data Source:** HN "Who Is Hiring", LinkedIn Jobs, GitHub
**Generated by:** Claude (Automated Analysis)

---

"""

    with open(filename, 'w') as f:
        f.write(header + insights)

    print(f"Saved insights to {filename}")
    return filename


def save_insights_to_snowflake(insights: str):
    """Save insights to Snowflake for historical tracking."""
    conn = get_snowflake_connection()
    cur = conn.cursor()

    # Create table if not exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS KOUVERK_DATA_INDUSTRY.weekly_insights (
        generated_at TIMESTAMP,
        insights_text VARCHAR,
        model VARCHAR
    )
    """)

    cur.execute("""
    INSERT INTO KOUVERK_DATA_INDUSTRY.weekly_insights
    (generated_at, insights_text, model)
    VALUES (%s, %s, %s)
    """, (datetime.utcnow(), insights, "claude-sonnet-4-20250514"))

    conn.commit()
    cur.close()
    conn.close()
    print("Saved insights to Snowflake")


def run_weekly_insights():
    """Main function to generate weekly insights."""
    print("Fetching technology trends...")
    tech_df = get_technology_trends()

    print("Fetching role trends...")
    role_df = get_role_trends()

    print("Fetching GitHub highlights...")
    github_df = get_github_highlights()

    print("Generating insights with Claude...")
    insights = generate_insights(tech_df, role_df, github_df)

    print("\n" + "="*60)
    print(insights)
    print("="*60 + "\n")

    # Save to file
    filepath = save_insights(insights)

    # Save to Snowflake
    save_insights_to_snowflake(insights)

    return insights, filepath


if __name__ == "__main__":
    run_weekly_insights()
