"""
Data & AI Industry Index Dashboard

Visualizes technology and role trends from HN job postings,
LinkedIn skills, and GitHub repo stats.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Data & AI Industry Index",
    page_icon="📊",
    layout="wide"
)

# Snowflake connection
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASSWORD'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA')
    )

@st.cache_data(ttl=600)
def run_query(query):
    conn = get_connection()
    return pd.read_sql(query, conn)

# =============================================================================
# HEADER
# =============================================================================
st.title("📊 Data & AI Industry Index")
st.markdown("*Tracking what's hot, growing, and dying in the data/AI space*")

# Data source disclaimers
with st.expander("ℹ️ Data Sources & Limitations"):
    st.markdown("""
    **Data Sources:**
    - **Hacker News "Who Is Hiring"** (2011-present): ~93K job postings from monthly hiring threads
    - **LinkedIn Jobs** (Jan 2024): 1.3M job postings snapshot from [Kaggle dataset](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024)
    - **GitHub Repository Stats**: 81 curated data/AI repositories tracked for stars, forks, activity

    **Known Limitations:**
    - **HN data skews toward startups and tech-native companies.** Enterprise/Fortune 500 hiring patterns may differ.
    - **LinkedIn data is a single cross-sectional snapshot (Jan 2024)**, not a time series. Trend claims are based on HN data only.
    - **GitHub repos are manually curated** based on relevance to data/AI ecosystem and minimum star thresholds.
    - **Skill extraction uses keyword matching**, which may miss context-dependent mentions or capture false positives.

    **Licensing:**
    - LinkedIn dataset used under Kaggle's terms for academic/research purposes only.
    - HN data is public via HuggingFace and HN Firebase API.
    - GitHub data accessed via public REST API.
    """)

st.markdown("---")

# =============================================================================
# SIDEBAR FILTERS
# =============================================================================
st.sidebar.header("Filters")

# Year range filter
min_year = 2018
max_year = 2025
year_range = st.sidebar.slider(
    "Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(2018, 2025)
)

# =============================================================================
# TECHNOLOGY TRENDS
# =============================================================================
st.header("🔧 Technology Trends")

# Get available technologies
tech_query = """
SELECT DISTINCT technology_name, category
FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
ORDER BY technology_name
"""
try:
    techs_df = run_query(tech_query)
    categories = ['All'] + sorted(techs_df['CATEGORY'].unique().tolist())

    col1, col2 = st.columns([1, 3])

    with col1:
        selected_category = st.selectbox("Category", categories)

        if selected_category == 'All':
            available_techs = techs_df['TECHNOLOGY_NAME'].tolist()
        else:
            available_techs = techs_df[techs_df['CATEGORY'] == selected_category]['TECHNOLOGY_NAME'].tolist()

        # Default interesting technologies
        default_techs = [t for t in ['Snowflake', 'Redshift', 'BigQuery', 'dbt', 'Airflow'] if t in available_techs]

        selected_techs = st.multiselect(
            "Technologies",
            options=available_techs,
            default=default_techs[:5]
        )

    with col2:
        if selected_techs:
            tech_list = "', '".join(selected_techs)
            trend_query = f"""
            SELECT
                posting_month,
                technology_name,
                mention_pct
            FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
            WHERE technology_name IN ('{tech_list}')
              AND EXTRACT(YEAR FROM posting_month) BETWEEN {year_range[0]} AND {year_range[1]}
            ORDER BY posting_month
            """
            trend_df = run_query(trend_query)

            if not trend_df.empty:
                fig = px.line(
                    trend_df,
                    x='POSTING_MONTH',
                    y='MENTION_PCT',
                    color='TECHNOLOGY_NAME',
                    title='Technology Mentions in HN Job Postings (% of posts)',
                    labels={'POSTING_MONTH': 'Month', 'MENTION_PCT': '% of Posts', 'TECHNOLOGY_NAME': 'Technology'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data for selected filters")
        else:
            st.info("Select technologies to view trends")

except Exception as e:
    st.error(f"Error loading technology data: {e}")

# =============================================================================
# ROLE TRENDS
# =============================================================================
st.header("👤 Role Trends")

try:
    role_query = """
    SELECT DISTINCT role_name, tier
    FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends
    ORDER BY tier, role_name
    """
    roles_df = run_query(role_query)

    col1, col2 = st.columns([1, 3])

    with col1:
        tiers = ['All'] + sorted(roles_df['TIER'].unique().tolist())
        selected_tier = st.selectbox("Role Tier", tiers)

        if selected_tier == 'All':
            available_roles = roles_df['ROLE_NAME'].tolist()
        else:
            available_roles = roles_df[roles_df['TIER'] == selected_tier]['ROLE_NAME'].tolist()

        default_roles = [r for r in ['Data Engineer', 'Analytics Engineer', 'Data Scientist', 'Machine Learning Engineer'] if r in available_roles]

        selected_roles = st.multiselect(
            "Roles",
            options=available_roles,
            default=default_roles[:4]
        )

    with col2:
        if selected_roles:
            role_list = "', '".join(selected_roles)
            role_trend_query = f"""
            SELECT
                posting_month,
                role_name,
                mention_pct
            FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends
            WHERE role_name IN ('{role_list}')
              AND EXTRACT(YEAR FROM posting_month) BETWEEN {year_range[0]} AND {year_range[1]}
            ORDER BY posting_month
            """
            role_trend_df = run_query(role_trend_query)

            if not role_trend_df.empty:
                fig = px.line(
                    role_trend_df,
                    x='POSTING_MONTH',
                    y='MENTION_PCT',
                    color='ROLE_NAME',
                    title='Role Mentions in HN Job Postings (% of posts)',
                    labels={'POSTING_MONTH': 'Month', 'MENTION_PCT': '% of Posts', 'ROLE_NAME': 'Role'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data for selected filters")
        else:
            st.info("Select roles to view trends")

except Exception as e:
    st.error(f"Error loading role data: {e}")

# =============================================================================
# GITHUB REPO STATS
# =============================================================================
st.header("⭐ GitHub Repository Stars")

try:
    github_query = """
    SELECT
        repo_name,
        full_name,
        category,
        stars,
        forks,
        activity_level,
        days_since_last_push
    FROM KOUVERK_DATA_INDUSTRY_marts.fct_github_repo_stats
    ORDER BY stars DESC
    """
    github_df = run_query(github_query)

    col1, col2 = st.columns(2)

    with col1:
        # Top repos bar chart
        top_n = 15
        fig = px.bar(
            github_df.head(top_n),
            x='STARS',
            y='REPO_NAME',
            orientation='h',
            color='CATEGORY',
            title=f'Top {top_n} Repos by Stars',
            labels={'STARS': 'Stars', 'REPO_NAME': 'Repository', 'CATEGORY': 'Category'}
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Most active repos - show stars for repos with recent activity
        active_repos = github_df.nsmallest(15, 'DAYS_SINCE_LAST_PUSH').copy()
        # Add activity label for display
        active_repos['ACTIVITY_LABEL'] = active_repos['REPO_NAME'] + ' (' + active_repos['DAYS_SINCE_LAST_PUSH'].astype(str) + 'd ago)'

        fig = px.bar(
            active_repos,
            x='STARS',
            y='REPO_NAME',
            orientation='h',
            color='ACTIVITY_LEVEL',
            title='Most Recently Active Repos (by stars)',
            labels={'STARS': 'Stars', 'REPO_NAME': 'Repository', 'ACTIVITY_LEVEL': 'Activity'},
            color_discrete_map={'Very Active': '#2ecc71', 'Active': '#3498db', 'Moderate': '#f39c12', 'Low Activity': '#e74c3c'}
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading GitHub data: {e}")

# =============================================================================
# LINKEDIN TOP SKILLS
# =============================================================================
st.header("💼 LinkedIn Top Skills (Jan 2024)")

try:
    linkedin_query = """
    SELECT
        skill_name,
        category,
        job_count,
        pct_of_jobs
    FROM KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts
    WHERE is_standardized = TRUE
    ORDER BY job_count DESC
    LIMIT 30
    """
    linkedin_df = run_query(linkedin_query)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            linkedin_df.head(15),
            x='JOB_COUNT',
            y='SKILL_NAME',
            orientation='h',
            color='CATEGORY',
            title='Top 15 Standardized Skills',
            labels={'JOB_COUNT': 'Job Count', 'SKILL_NAME': 'Skill', 'CATEGORY': 'Category'}
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top roles by job mentions from HN data
        role_query = """
        SELECT
            role_name,
            tier,
            SUM(mention_count) as total_mentions
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends
        GROUP BY role_name, tier
        ORDER BY total_mentions DESC
        LIMIT 15
        """
        role_df = run_query(role_query)

        fig = px.bar(
            role_df,
            x='TOTAL_MENTIONS',
            y='ROLE_NAME',
            orientation='h',
            color='TIER',
            title='Top Roles by Job Mentions (HN)',
            labels={'TOTAL_MENTIONS': 'Total Mentions', 'ROLE_NAME': 'Role', 'TIER': 'Tier'}
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading LinkedIn data: {e}")

# =============================================================================
# YEAR-OVER-YEAR COMPARISON
# =============================================================================
st.header("📈 Year-over-Year Comparison")

try:
    yoy_query = f"""
    WITH yearly AS (
        SELECT
            EXTRACT(YEAR FROM posting_month) as year,
            technology_name,
            AVG(mention_pct) as avg_mention_pct
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
        WHERE EXTRACT(YEAR FROM posting_month) IN ({year_range[1]-1}, {year_range[1]})
        GROUP BY 1, 2
    ),
    pivoted AS (
        SELECT
            technology_name,
            MAX(CASE WHEN year = {year_range[1]-1} THEN avg_mention_pct END) as prev_year,
            MAX(CASE WHEN year = {year_range[1]} THEN avg_mention_pct END) as curr_year
        FROM yearly
        GROUP BY 1
    )
    SELECT
        technology_name,
        prev_year,
        curr_year,
        curr_year - prev_year as change,
        CASE WHEN prev_year > 0 THEN ((curr_year - prev_year) / prev_year * 100) ELSE NULL END as pct_change
    FROM pivoted
    WHERE prev_year IS NOT NULL AND curr_year IS NOT NULL
    ORDER BY change DESC
    """
    yoy_df = run_query(yoy_query)

    if not yoy_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"🚀 Biggest Gainers ({year_range[1]-1} → {year_range[1]})")
            gainers = yoy_df.head(10)
            fig = px.bar(
                gainers,
                x='CHANGE',
                y='TECHNOLOGY_NAME',
                orientation='h',
                color='CHANGE',
                color_continuous_scale='Greens',
                title='Top 10 Growing Technologies',
                labels={'CHANGE': 'Change in % of Posts', 'TECHNOLOGY_NAME': 'Technology'}
            )
            fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader(f"📉 Biggest Decliners ({year_range[1]-1} → {year_range[1]})")
            decliners = yoy_df.tail(10).sort_values('CHANGE')
            fig = px.bar(
                decliners,
                x='CHANGE',
                y='TECHNOLOGY_NAME',
                orientation='h',
                color='CHANGE',
                color_continuous_scale='Reds_r',
                title='Top 10 Declining Technologies',
                labels={'CHANGE': 'Change in % of Posts', 'TECHNOLOGY_NAME': 'Technology'}
            )
            fig.update_layout(height=400, yaxis={'categoryorder': 'total descending'}, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error loading YoY data: {e}")

# =============================================================================
# RAW DATA EXPLORER
# =============================================================================
st.header("🔍 Data Explorer")

with st.expander("Explore Raw Data"):
    table_options = {
        'Technology Trends': 'KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends',
        'Role Trends': 'KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends',
        'GitHub Stats': 'KOUVERK_DATA_INDUSTRY_marts.fct_github_repo_stats',
        'LinkedIn Skills': 'KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts'
    }

    selected_table = st.selectbox("Select Table", list(table_options.keys()))

    if st.button("Load Data"):
        query = f"SELECT * FROM {table_options[selected_table]} LIMIT 1000"
        df = run_query(query)
        st.dataframe(df, use_container_width=True)

        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{selected_table.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )

# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
**Data Sources:**
- HN "Who Is Hiring" (2011-present): 93K+ job postings
- LinkedIn Jobs (Jan 2024): 1.3M job postings
- GitHub API: 81 data/AI repositories

*Built with Streamlit, dbt, Snowflake, and Airflow*
""")
