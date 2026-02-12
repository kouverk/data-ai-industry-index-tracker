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
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# DATABASE CONNECTION
# =============================================================================

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
# PAGE: EXECUTIVE SUMMARY
# =============================================================================

def render_executive_summary():
    """Executive summary with key metrics and findings."""
    st.title("📊 Data & AI Industry Index")
    st.markdown("*Tracking what's hot, growing, and dying in the data/AI space*")

    # Key metrics row
    try:
        metrics_query = """
        SELECT
            (SELECT COUNT(*) FROM KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings) as hn_posts,
            (SELECT COUNT(*) FROM KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__postings) as linkedin_jobs,
            (SELECT COUNT(*) FROM KOUVERK_DATA_INDUSTRY_marts.fct_github_repo_stats) as github_repos,
            (SELECT COUNT(DISTINCT technology_name) FROM KOUVERK_DATA_INDUSTRY_marts.dim_technologies) as technologies,
            (SELECT COUNT(DISTINCT role_name) FROM KOUVERK_DATA_INDUSTRY_marts.dim_roles) as roles
        """
        metrics = run_query(metrics_query)

        if not metrics.empty:
            row = metrics.iloc[0]
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("HN Job Postings", f"{int(row['HN_POSTS']):,}")
            col2.metric("LinkedIn Jobs", f"{int(row['LINKEDIN_JOBS']):,}")
            col3.metric("GitHub Repos", f"{int(row['GITHUB_REPOS'])}")
            col4.metric("Technologies Tracked", f"{int(row['TECHNOLOGIES'])}")
            col5.metric("Roles Tracked", f"{int(row['ROLES'])}")
    except Exception as e:
        st.error(f"Error loading metrics: {e}")

    st.divider()

    # Key Findings
    st.subheader("Key Findings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        | Finding | Evidence |
        |---------|----------|
        | **Snowflake overtook Redshift** | 1.6% vs 0.4% of HN posts in 2024 (crossed in 2022) |
        | **PyTorch dominates TensorFlow** | 2.0% vs 0.5% in 2025 (4x lead, flipped 2022) |
        | **OpenAI mentions exploded** | 0.4% → 2.7% (2022-2025) |
        """)

    with col2:
        st.markdown("""
        | Finding | Evidence |
        |---------|----------|
        | **LLM extracts 4x more skills** | 6.4 vs 1.5 technologies/post |
        | **PostgreSQL is king** | 14% of HN posts 2024-25 (6x next DB) |
        | **2021 was peak hiring** | 10,570 posts; 2023-24 ~40% of peak |
        """)

    st.divider()

    # Quick trend visualization
    st.subheader("Technology Trends at a Glance")

    try:
        trend_query = """
        SELECT
            posting_month,
            technology_name,
            mention_pct
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
        WHERE technology_name IN ('Snowflake', 'Redshift', 'BigQuery', 'Databricks')
          AND EXTRACT(YEAR FROM posting_month) >= 2018
        ORDER BY posting_month
        """
        trend_df = run_query(trend_query)

        if not trend_df.empty:
            fig = px.line(
                trend_df,
                x='POSTING_MONTH',
                y='MENTION_PCT',
                color='TECHNOLOGY_NAME',
                title='Cloud Data Warehouse Wars (2018-Present)',
                labels={'POSTING_MONTH': 'Month', 'MENTION_PCT': '% of Posts', 'TECHNOLOGY_NAME': 'Technology'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error loading trends: {e}")

    # Hiring volume over time
    try:
        volume_query = """
        SELECT
            EXTRACT(YEAR FROM posting_month) as year,
            SUM(total_postings) as total_postings
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
        WHERE technology_name = 'Python'
        GROUP BY 1
        ORDER BY 1
        """
        volume_df = run_query(volume_query)

        if not volume_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(
                    volume_df,
                    x='YEAR',
                    y='TOTAL_POSTINGS',
                    title='HN Job Posting Volume by Year',
                    labels={'YEAR': 'Year', 'TOTAL_POSTINGS': 'Posts'}
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # LLM extraction summary
                llm_query = """
                SELECT
                    COUNT(*) as total_posts,
                    SUM(CASE WHEN is_successful THEN 1 ELSE 0 END) as successful,
                    ROUND(SUM(CASE WHEN is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as success_rate,
                    AVG(CASE WHEN is_successful THEN technology_count END) as avg_techs
                FROM KOUVERK_DATA_INDUSTRY_staging.stg_llm__skill_extractions
                """
                llm_summary = run_query(llm_query)

                if not llm_summary.empty:
                    llm_row = llm_summary.iloc[0]
                    st.markdown("**LLM Extraction Performance**")
                    st.metric("Posts Processed", f"{int(llm_row['TOTAL_POSTS']):,}")
                    st.metric("Success Rate", f"{llm_row['SUCCESS_RATE']}%")
                    st.metric("Avg Techs/Post (LLM)", f"{llm_row['AVG_TECHS']:.1f}")
                    st.caption("vs ~1.5 techs/post with regex")
    except Exception as e:
        st.error(f"Error loading volume data: {e}")


# =============================================================================
# PAGE: TECHNOLOGY TRENDS
# =============================================================================

def render_technology_trends(year_range):
    """Technology trends over time."""
    st.header("🔧 Technology Trends")
    st.markdown("*Track technology mentions in Hacker News job postings over time*")

    try:
        tech_query = """
        SELECT DISTINCT technology_name, category
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
        ORDER BY technology_name
        """
        techs_df = run_query(tech_query)
        categories = ['All'] + sorted(techs_df['CATEGORY'].unique().tolist())

        col1, col2 = st.columns([1, 3])

        with col1:
            selected_category = st.selectbox("Category", categories)

            if selected_category == 'All':
                available_techs = techs_df['TECHNOLOGY_NAME'].tolist()
            else:
                available_techs = techs_df[techs_df['CATEGORY'] == selected_category]['TECHNOLOGY_NAME'].tolist()

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
                    fig.update_layout(height=450)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data for selected filters")
            else:
                st.info("Select technologies to view trends")

        # Year-over-Year comparison
        st.subheader("Year-over-Year Comparison")

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
            curr_year - prev_year as change
        FROM pivoted
        WHERE prev_year IS NOT NULL AND curr_year IS NOT NULL
        ORDER BY change DESC
        """
        yoy_df = run_query(yoy_query)

        if not yoy_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**Biggest Gainers ({year_range[1]-1} → {year_range[1]})**")
                gainers = yoy_df.head(10)
                fig = px.bar(
                    gainers,
                    x='CHANGE',
                    y='TECHNOLOGY_NAME',
                    orientation='h',
                    color='CHANGE',
                    color_continuous_scale='Greens',
                    labels={'CHANGE': 'Change in % of Posts', 'TECHNOLOGY_NAME': 'Technology'}
                )
                fig.update_layout(height=350, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown(f"**Biggest Decliners ({year_range[1]-1} → {year_range[1]})**")
                decliners = yoy_df.tail(10).sort_values('CHANGE')
                fig = px.bar(
                    decliners,
                    x='CHANGE',
                    y='TECHNOLOGY_NAME',
                    orientation='h',
                    color='CHANGE',
                    color_continuous_scale='Reds_r',
                    labels={'CHANGE': 'Change in % of Posts', 'TECHNOLOGY_NAME': 'Technology'}
                )
                fig.update_layout(height=350, yaxis={'categoryorder': 'total descending'}, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

        # Technology Co-occurrence Analysis
        st.divider()
        st.subheader("Technology Co-occurrence")
        st.markdown("*Which technologies appear together in job postings?*")

        # Let user select a technology to see what it's commonly paired with
        cooc_base_query = """
        SELECT DISTINCT technology_name
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions
        ORDER BY technology_name
        """
        cooc_techs_df = run_query(cooc_base_query)

        if not cooc_techs_df.empty:
            col1, col2 = st.columns([1, 3])

            with col1:
                tech_options = cooc_techs_df['TECHNOLOGY_NAME'].tolist()
                default_tech = 'Snowflake' if 'Snowflake' in tech_options else tech_options[0]
                selected_cooc_tech = st.selectbox(
                    "Select a technology",
                    options=tech_options,
                    index=tech_options.index(default_tech),
                    key="cooc_tech_select"
                )

            with col2:
                if selected_cooc_tech:
                    cooc_query = f"""
                    WITH base_posts AS (
                        SELECT DISTINCT posting_id
                        FROM KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions
                        WHERE technology_name = '{selected_cooc_tech}'
                    ),
                    paired_techs AS (
                        SELECT
                            m.technology_name,
                            COUNT(DISTINCT m.posting_id) as co_occurrence_count
                        FROM KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions m
                        INNER JOIN base_posts b ON m.posting_id = b.posting_id
                        WHERE m.technology_name != '{selected_cooc_tech}'
                        GROUP BY m.technology_name
                    )
                    SELECT
                        technology_name,
                        co_occurrence_count,
                        ROUND(co_occurrence_count * 100.0 / (SELECT COUNT(*) FROM base_posts), 1) as pct_of_base
                    FROM paired_techs
                    ORDER BY co_occurrence_count DESC
                    LIMIT 15
                    """
                    cooc_df = run_query(cooc_query)

                    if not cooc_df.empty:
                        fig = px.bar(
                            cooc_df,
                            x='CO_OCCURRENCE_COUNT',
                            y='TECHNOLOGY_NAME',
                            orientation='h',
                            color='PCT_OF_BASE',
                            color_continuous_scale='Blues',
                            title=f'Top Technologies Appearing with {selected_cooc_tech}',
                            labels={
                                'CO_OCCURRENCE_COUNT': 'Co-occurrences',
                                'TECHNOLOGY_NAME': 'Technology',
                                'PCT_OF_BASE': '% of Posts'
                            },
                            hover_data=['PCT_OF_BASE']
                        )
                        fig.update_layout(height=450, yaxis={'categoryorder': 'total ascending'})
                        st.plotly_chart(fig, use_container_width=True)

                        st.caption(f"Shows technologies that appear in the same job postings as {selected_cooc_tech}")
                    else:
                        st.info("No co-occurrence data found")

            # Popular technology pairs
            st.markdown("### Top Technology Pairs")
            st.markdown("*Most common technology combinations across all job postings*")

            pairs_query = """
            WITH tech_pairs AS (
                SELECT
                    a.technology_name as tech_a,
                    b.technology_name as tech_b,
                    COUNT(DISTINCT a.posting_id) as pair_count
                FROM KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions a
                INNER JOIN KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions b
                    ON a.posting_id = b.posting_id
                    AND a.technology_name < b.technology_name
                GROUP BY a.technology_name, b.technology_name
            )
            SELECT
                tech_a || ' + ' || tech_b as tech_pair,
                tech_a,
                tech_b,
                pair_count
            FROM tech_pairs
            ORDER BY pair_count DESC
            LIMIT 20
            """
            pairs_df = run_query(pairs_query)

            if not pairs_df.empty:
                fig = px.bar(
                    pairs_df,
                    x='PAIR_COUNT',
                    y='TECH_PAIR',
                    orientation='h',
                    title='Top 20 Technology Pairs in Job Postings',
                    labels={'PAIR_COUNT': 'Co-occurrences', 'TECH_PAIR': 'Technology Pair'},
                    color='PAIR_COUNT',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=550, yaxis={'categoryorder': 'total ascending'}, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading technology data: {e}")


# =============================================================================
# PAGE: ROLE TRENDS
# =============================================================================

def render_role_trends(year_range):
    """Role trends over time."""
    st.header("👤 Role Trends")
    st.markdown("*Track data/AI role mentions in Hacker News job postings*")

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
                    fig.update_layout(height=450)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data for selected filters")
            else:
                st.info("Select roles to view trends")

        # Top roles by total mentions
        st.subheader("Top Roles by Total Mentions")

        top_roles_query = """
        SELECT
            role_name,
            tier,
            SUM(mention_count) as total_mentions
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends
        GROUP BY role_name, tier
        ORDER BY total_mentions DESC
        LIMIT 15
        """
        top_roles_df = run_query(top_roles_query)

        if not top_roles_df.empty:
            fig = px.bar(
                top_roles_df,
                x='TOTAL_MENTIONS',
                y='ROLE_NAME',
                orientation='h',
                color='TIER',
                title='Top Roles by Total Job Mentions (HN)',
                labels={'TOTAL_MENTIONS': 'Total Mentions', 'ROLE_NAME': 'Role', 'TIER': 'Tier'}
            )
            fig.update_layout(height=450, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading role data: {e}")


# =============================================================================
# PAGE: GITHUB & LINKEDIN
# =============================================================================

def render_github_linkedin():
    """GitHub repo stats and LinkedIn skill counts."""
    st.header("⭐ GitHub & LinkedIn Data")
    st.markdown("*Cross-sectional views of repository activity and skill demand*")

    tab1, tab2, tab3 = st.tabs(["GitHub Repos", "LinkedIn Skills", "HN vs LinkedIn Comparison"])

    with tab1:
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
                active_repos = github_df.nsmallest(15, 'DAYS_SINCE_LAST_PUSH').copy()
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

    with tab2:
        st.markdown("**LinkedIn Skills (January 2024 Snapshot)**")
        st.caption("From Kaggle dataset of 1.3M job postings")

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

            if not linkedin_df.empty:
                fig = px.bar(
                    linkedin_df.head(20),
                    x='JOB_COUNT',
                    y='SKILL_NAME',
                    orientation='h',
                    color='CATEGORY',
                    title='Top 20 Standardized Skills (LinkedIn)',
                    labels={'JOB_COUNT': 'Job Count', 'SKILL_NAME': 'Skill', 'CATEGORY': 'Category'}
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error loading LinkedIn data: {e}")

    with tab3:
        st.markdown("**HN vs LinkedIn: Do Startup Trends Match the Broader Market?**")
        st.caption("Comparing skill demand between HN (startup-focused) and LinkedIn (enterprise-focused)")

        try:
            # Get HN top skills (2024 data to match LinkedIn snapshot)
            hn_query = """
            SELECT
                technology_name as skill,
                ROUND(AVG(mention_pct), 2) as hn_pct,
                'HN 2024' as source
            FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
            WHERE EXTRACT(YEAR FROM posting_month) = 2024
            GROUP BY 1
            HAVING AVG(mention_pct) >= 0.5
            ORDER BY 2 DESC
            LIMIT 25
            """
            hn_df = run_query(hn_query)

            # Get LinkedIn top skills (standardized only)
            linkedin_query = """
            SELECT
                skill_name as skill,
                pct_of_jobs as linkedin_pct,
                'LinkedIn' as source
            FROM KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts
            WHERE is_standardized = TRUE
              AND pct_of_jobs >= 0.5
            ORDER BY pct_of_jobs DESC
            LIMIT 25
            """
            linkedin_df = run_query(linkedin_query)

            if not hn_df.empty and not linkedin_df.empty:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### Top Skills: HN (2024)")
                    fig = px.bar(
                        hn_df.head(15),
                        x='HN_PCT',
                        y='SKILL',
                        orientation='h',
                        title='Top 15 Technologies in HN Job Posts',
                        labels={'HN_PCT': '% of Posts', 'SKILL': 'Technology'},
                        color_discrete_sequence=['#e74c3c']
                    )
                    fig.update_layout(height=450, yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown("### Top Skills: LinkedIn (Jan 2024)")
                    fig = px.bar(
                        linkedin_df.head(15),
                        x='LINKEDIN_PCT',
                        y='SKILL',
                        orientation='h',
                        title='Top 15 Skills in LinkedIn Job Posts',
                        labels={'LINKEDIN_PCT': '% of Jobs', 'SKILL': 'Skill'},
                        color_discrete_sequence=['#3498db']
                    )
                    fig.update_layout(height=450, yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)

                # Find overlapping skills for direct comparison
                st.divider()
                st.markdown("### Direct Comparison: Skills in Both Datasets")

                # Join the datasets on skill name
                hn_skills = set(hn_df['SKILL'].str.lower())
                linkedin_skills = set(linkedin_df['SKILL'].str.lower())
                common_skills = hn_skills.intersection(linkedin_skills)

                if common_skills:
                    comparison_query = f"""
                    WITH hn_data AS (
                        SELECT
                            technology_name as skill,
                            ROUND(AVG(mention_pct), 2) as pct
                        FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
                        WHERE EXTRACT(YEAR FROM posting_month) = 2024
                        GROUP BY 1
                    ),
                    linkedin_data AS (
                        SELECT
                            skill_name as skill,
                            pct_of_jobs as pct
                        FROM KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts
                        WHERE is_standardized = TRUE
                    )
                    SELECT
                        h.skill,
                        h.pct as hn_pct,
                        l.pct as linkedin_pct,
                        h.pct - l.pct as diff
                    FROM hn_data h
                    INNER JOIN linkedin_data l ON LOWER(h.skill) = LOWER(l.skill)
                    WHERE h.pct >= 0.3 OR l.pct >= 0.3
                    ORDER BY ABS(h.pct - l.pct) DESC
                    LIMIT 15
                    """
                    comparison_df = run_query(comparison_query)

                    if not comparison_df.empty:
                        # Create a diverging bar chart
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            y=comparison_df['SKILL'],
                            x=comparison_df['HN_PCT'],
                            name='HN (Startups)',
                            orientation='h',
                            marker_color='#e74c3c'
                        ))
                        fig.add_trace(go.Bar(
                            y=comparison_df['SKILL'],
                            x=comparison_df['LINKEDIN_PCT'],
                            name='LinkedIn (Enterprise)',
                            orientation='h',
                            marker_color='#3498db'
                        ))
                        fig.update_layout(
                            barmode='group',
                            title='HN vs LinkedIn: Same Skills, Different Demand',
                            xaxis_title='% of Job Posts',
                            yaxis_title='Skill/Technology',
                            height=500,
                            yaxis={'categoryorder': 'total ascending'}
                        )
                        st.plotly_chart(fig, use_container_width=True)

                        st.markdown("""
                        **Key Observations:**
                        - Higher HN % = more popular in startups/tech companies
                        - Higher LinkedIn % = more popular in enterprise/traditional companies
                        - Large differences indicate startup vs enterprise preference
                        """)
                else:
                    st.info("No overlapping skills found between datasets")

        except Exception as e:
            st.error(f"Error loading comparison data: {e}")


# =============================================================================
# PAGE: LLM VS REGEX ANALYSIS
# =============================================================================

def render_llm_analysis():
    """LLM vs Regex skill extraction comparison."""
    st.header("🤖 LLM vs Regex Skill Extraction")
    st.markdown("*Comparing Claude Haiku extraction against regex keyword matching on a 10K post sample*")

    try:
        # Summary metrics
        llm_summary_query = """
        SELECT
            COUNT(*) as total_posts,
            SUM(CASE WHEN is_successful THEN 1 ELSE 0 END) as successful,
            ROUND(SUM(CASE WHEN is_successful THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as success_rate,
            AVG(CASE WHEN is_successful THEN technology_count END) as avg_techs,
            AVG(CASE WHEN is_successful THEN role_count END) as avg_roles,
            SUM(CASE WHEN is_successful THEN technology_count ELSE 0 END) as total_tech_mentions
        FROM KOUVERK_DATA_INDUSTRY_staging.stg_llm__skill_extractions
        """
        llm_summary = run_query(llm_summary_query)

        if not llm_summary.empty:
            row = llm_summary.iloc[0]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Posts Processed", f"{int(row['TOTAL_POSTS']):,}")
            col2.metric("Success Rate", f"{row['SUCCESS_RATE']}%")
            col3.metric("Avg Techs/Post (LLM)", f"{row['AVG_TECHS']:.1f}", delta="vs 1.5 regex")
            col4.metric("Total Tech Mentions", f"{int(row['TOTAL_TECH_MENTIONS']):,}")

        st.divider()

        # Comparison data
        comparison_query = """
        SELECT *
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_llm_vs_regex_comparison
        ORDER BY total_postings DESC
        """
        comp_df = run_query(comparison_query)

        if not comp_df.empty:
            col1, col2 = st.columns(2)

            with col1:
                top_techs = comp_df.head(30).copy()
                fig = px.scatter(
                    top_techs,
                    x='AGREEMENT_PCT',
                    y='TECHNOLOGY_NAME',
                    size='TOTAL_POSTINGS',
                    color='CATEGORY',
                    title='LLM vs Regex Agreement Rate (Top 30 Technologies)',
                    labels={
                        'AGREEMENT_PCT': 'Agreement %',
                        'TECHNOLOGY_NAME': 'Technology',
                        'TOTAL_POSTINGS': 'Total Postings',
                        'CATEGORY': 'Category'
                    }
                )
                fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                top_techs_bar = comp_df.head(20).copy()
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    y=top_techs_bar['TECHNOLOGY_NAME'],
                    x=top_techs_bar['LLM_ONLY_COUNT'],
                    name='LLM Only',
                    orientation='h',
                    marker_color='#e74c3c'
                ))
                fig.add_trace(go.Bar(
                    y=top_techs_bar['TECHNOLOGY_NAME'],
                    x=top_techs_bar['BOTH_COUNT'],
                    name='Both Methods',
                    orientation='h',
                    marker_color='#2ecc71'
                ))
                fig.add_trace(go.Bar(
                    y=top_techs_bar['TECHNOLOGY_NAME'],
                    x=top_techs_bar['REGEX_ONLY_COUNT'],
                    name='Regex Only',
                    orientation='h',
                    marker_color='#3498db'
                ))
                fig.update_layout(
                    barmode='stack',
                    title='Detection Method Breakdown (Top 20)',
                    xaxis_title='Number of Postings',
                    yaxis_title='Technology',
                    height=600,
                    yaxis={'categoryorder': 'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True)

            # LLM-only discoveries
            st.subheader("Technologies Found Only by LLM")
            st.markdown("*Technologies the LLM detected that aren't in the regex taxonomy*")

            llm_only_query = """
            SELECT
                technology_name,
                category,
                llm_count as mentions,
                avg_llm_confidence as confidence
            FROM KOUVERK_DATA_INDUSTRY_marts.fct_llm_vs_regex_comparison
            WHERE regex_count = 0
            ORDER BY llm_count DESC
            LIMIT 20
            """
            llm_only_df = run_query(llm_only_query)

            if not llm_only_df.empty:
                fig = px.bar(
                    llm_only_df,
                    x='MENTIONS',
                    y='TECHNOLOGY_NAME',
                    orientation='h',
                    color='CONFIDENCE',
                    color_continuous_scale='Viridis',
                    title='Top 20 LLM-Only Technologies (Not in Regex Taxonomy)',
                    labels={
                        'MENTIONS': 'Postings Mentioned',
                        'TECHNOLOGY_NAME': 'Technology',
                        'CONFIDENCE': 'Avg Confidence'
                    }
                )
                fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)

            # Summary table
            st.subheader("Method Comparison Summary")
            st.markdown("""
            | Dimension | LLM (Claude Haiku) | Regex (Keyword Match) |
            |-----------|--------------------|-----------------------|
            | **Coverage** | 4,569 unique technologies | 152 curated technologies |
            | **Avg Techs/Post** | 6.4 | 1.5 |
            | **Cost** | $0.00045/post | Free |
            | **Speed** | ~25 min for 10K | Instant on full 93K |
            | **Maintenance** | None (model handles variations) | Manual (update seed CSVs) |
            """)

        # Time-series of LLM-extracted technologies
        st.divider()
        st.subheader("LLM Technology Trends Over Time")
        st.markdown("*How do LLM-extracted technologies trend within the 10K post sample?*")

        # Get top technologies from LLM data for selection
        top_llm_techs_query = """
        SELECT
            technology_name,
            COUNT(*) as mention_count
        FROM KOUVERK_DATA_INDUSTRY_marts.fct_llm_technology_mentions
        GROUP BY technology_name
        ORDER BY mention_count DESC
        LIMIT 50
        """
        top_llm_techs = run_query(top_llm_techs_query)

        if not top_llm_techs.empty:
            available_techs = top_llm_techs['TECHNOLOGY_NAME'].tolist()
            default_techs = [t for t in ['Python', 'PostgreSQL', 'AWS', 'React', 'TypeScript', 'Docker'] if t in available_techs]

            col1, col2 = st.columns([1, 3])

            with col1:
                selected_llm_techs = st.multiselect(
                    "Select technologies",
                    options=available_techs,
                    default=default_techs[:5],
                    key="llm_tech_multiselect"
                )

            with col2:
                if selected_llm_techs:
                    tech_list = "', '".join(selected_llm_techs)
                    llm_trend_query = f"""
                    SELECT
                        posting_month,
                        technology_name,
                        COUNT(*) as mention_count
                    FROM KOUVERK_DATA_INDUSTRY_marts.fct_llm_technology_mentions
                    WHERE technology_name IN ('{tech_list}')
                    GROUP BY posting_month, technology_name
                    ORDER BY posting_month
                    """
                    llm_trend_df = run_query(llm_trend_query)

                    if not llm_trend_df.empty:
                        fig = px.line(
                            llm_trend_df,
                            x='POSTING_MONTH',
                            y='MENTION_COUNT',
                            color='TECHNOLOGY_NAME',
                            title='LLM-Extracted Technology Mentions by Month (10K Sample)',
                            labels={
                                'POSTING_MONTH': 'Month',
                                'MENTION_COUNT': 'Mentions',
                                'TECHNOLOGY_NAME': 'Technology'
                            },
                            markers=True
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No trend data for selected technologies")
                else:
                    st.info("Select technologies to view LLM extraction trends")

            # Show monthly sample distribution
            st.caption("Note: This reflects the 10K post sample distribution, which may not be uniform across months.")

            # Side-by-side comparison for overlapping technologies
            st.divider()
            st.subheader("LLM vs Regex: Side-by-Side Trend Comparison")
            st.markdown("*Compare extraction methods for technologies in both taxonomies*")

            # Get technologies that appear in both LLM and regex
            overlapping_query = """
            SELECT technology_name, both_count
            FROM KOUVERK_DATA_INDUSTRY_marts.fct_llm_vs_regex_comparison
            WHERE both_count > 50
            ORDER BY both_count DESC
            LIMIT 20
            """
            overlapping_df = run_query(overlapping_query)

            if not overlapping_df.empty:
                overlap_techs = overlapping_df['TECHNOLOGY_NAME'].tolist()
                default_overlap = [t for t in ['Python', 'PostgreSQL', 'AWS', 'Kafka', 'Spark'] if t in overlap_techs]

                selected_overlap_tech = st.selectbox(
                    "Select technology to compare",
                    options=overlap_techs,
                    index=overlap_techs.index(default_overlap[0]) if default_overlap else 0,
                    key="overlap_tech_select"
                )

                if selected_overlap_tech:
                    # Get LLM trend
                    llm_single_query = f"""
                    SELECT
                        posting_month,
                        COUNT(*) as mention_count,
                        'LLM' as method
                    FROM KOUVERK_DATA_INDUSTRY_marts.fct_llm_technology_mentions
                    WHERE LOWER(technology_name) = LOWER('{selected_overlap_tech}')
                    GROUP BY posting_month
                    """
                    llm_single_df = run_query(llm_single_query)

                    # Get Regex trend (from fct_monthly_technology_trends)
                    regex_single_query = f"""
                    SELECT
                        posting_month,
                        mention_count,
                        'Regex' as method
                    FROM KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends
                    WHERE LOWER(technology_name) = LOWER('{selected_overlap_tech}')
                    """
                    regex_single_df = run_query(regex_single_query)

                    # Combine for comparison chart
                    if not llm_single_df.empty or not regex_single_df.empty:
                        combined_df = pd.concat([llm_single_df, regex_single_df], ignore_index=True)
                        combined_df = combined_df.sort_values('POSTING_MONTH')

                        if not combined_df.empty:
                            fig = px.line(
                                combined_df,
                                x='POSTING_MONTH',
                                y='MENTION_COUNT',
                                color='METHOD',
                                title=f'{selected_overlap_tech}: LLM vs Regex Extraction Over Time',
                                labels={
                                    'POSTING_MONTH': 'Month',
                                    'MENTION_COUNT': 'Mentions',
                                    'METHOD': 'Method'
                                },
                                markers=True,
                                color_discrete_map={'LLM': '#e74c3c', 'Regex': '#3498db'}
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)

                            st.caption("LLM data covers 10K posts; Regex data covers full 93K posts. Compare relative shapes, not absolute counts.")

    except Exception as e:
        st.error(f"Error loading LLM comparison data: {e}")


# =============================================================================
# PAGE: DATA EXPLORER
# =============================================================================

def render_data_explorer():
    """Raw data exploration."""
    st.header("🔍 Data Explorer")
    st.markdown("*Explore the underlying data tables*")

    table_options = {
        'Technology Trends': 'KOUVERK_DATA_INDUSTRY_marts.fct_monthly_technology_trends',
        'Role Trends': 'KOUVERK_DATA_INDUSTRY_marts.fct_monthly_role_trends',
        'GitHub Stats': 'KOUVERK_DATA_INDUSTRY_marts.fct_github_repo_stats',
        'LinkedIn Skills': 'KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts',
        'LLM Technology Mentions': 'KOUVERK_DATA_INDUSTRY_marts.fct_llm_technology_mentions',
        'LLM vs Regex Comparison': 'KOUVERK_DATA_INDUSTRY_marts.fct_llm_vs_regex_comparison',
        'Technologies Dimension': 'KOUVERK_DATA_INDUSTRY_marts.dim_technologies',
        'Roles Dimension': 'KOUVERK_DATA_INDUSTRY_marts.dim_roles'
    }

    selected_table = st.selectbox("Select Table", list(table_options.keys()))

    col1, col2 = st.columns([1, 4])
    with col1:
        limit = st.number_input("Row Limit", min_value=100, max_value=10000, value=1000, step=100)

    if st.button("Load Data"):
        try:
            query = f"SELECT * FROM {table_options[selected_table]} LIMIT {limit}"
            df = run_query(query)
            st.dataframe(df, use_container_width=True, height=500)

            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{selected_table.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error loading data: {e}")

    # Job Posting Search
    st.divider()
    st.subheader("🔎 Job Posting Search")
    st.markdown("*Search the raw HN job postings for specific keywords*")

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "Search term",
            placeholder="e.g., 'Snowflake', 'remote', 'Series A'",
            key="job_search_term"
        )

    with col2:
        year_filter = st.selectbox(
            "Year",
            options=['All'] + list(range(2025, 2010, -1)),
            key="job_search_year"
        )

    with col3:
        result_limit = st.selectbox(
            "Max results",
            options=[10, 25, 50, 100],
            index=1,
            key="job_search_limit"
        )

    if st.button("Search Posts", key="search_posts_btn"):
        if search_term:
            try:
                # Build query with search term
                year_clause = ""
                if year_filter != 'All':
                    year_clause = f"AND posting_year = {year_filter}"

                # Escape single quotes in search term
                safe_search = search_term.replace("'", "''")

                search_query = f"""
                SELECT
                    posting_id,
                    posting_month,
                    posting_year,
                    LEFT(posting_text, 500) as post_preview,
                    LENGTH(posting_text) as full_length
                FROM KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
                WHERE LOWER(posting_text) LIKE LOWER('%{safe_search}%')
                {year_clause}
                ORDER BY posting_month DESC
                LIMIT {result_limit}
                """
                search_results = run_query(search_query)

                if not search_results.empty:
                    st.success(f"Found {len(search_results)} posts containing '{search_term}'")

                    for idx, row in search_results.iterrows():
                        with st.expander(f"📄 Post from {row['POSTING_MONTH']} (ID: {row['POSTING_ID'][:8]}...)"):
                            # Highlight the search term in the preview
                            preview = row['POST_PREVIEW']
                            st.markdown(f"**Preview:** {preview}...")
                            if row['FULL_LENGTH'] > 500:
                                st.caption(f"Showing first 500 of {row['FULL_LENGTH']} characters")
                else:
                    st.warning(f"No posts found containing '{search_term}'")

            except Exception as e:
                st.error(f"Search error: {e}")
        else:
            st.info("Enter a search term to find job postings")


# =============================================================================
# PAGE: METHODOLOGY
# =============================================================================

def render_methodology():
    """Methodology, data sources, and pipeline explanation."""
    st.header("📚 Methodology")
    st.markdown("*How this project collects, processes, and analyzes data*")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Sources", "Pipeline", "Skill Extraction", "Taxonomy", "Limitations"])

    with tab1:
        st.subheader("Data Sources")

        st.markdown("### Hacker News 'Who Is Hiring'")
        st.markdown("""
        - **What:** Monthly job posting threads on Hacker News (first-level comments)
        - **Volume:** 93K+ job postings from 2011-present
        - **Source:** [HuggingFace dataset](https://huggingface.co/datasets/brusic/hacker-news-who-is-hiring-posts)
        - **Update frequency:** Monthly (threads close after 2 weeks)
        - **Strengths:** Long time series, tech-focused, startup-heavy
        - **Limitations:** Skews toward startups and US tech hubs; not representative of enterprise hiring
        """)

        st.markdown("### LinkedIn Jobs")
        st.markdown("""
        - **What:** Job postings with pre-extracted skills
        - **Volume:** 1.3M job postings
        - **Source:** [Kaggle dataset](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024) (January 2024 snapshot)
        - **Strengths:** Large scale, diverse industries, pre-extracted skills
        - **Limitations:** Single point-in-time snapshot (no time series), academic use only
        """)

        st.markdown("### GitHub Repository Stats")
        st.markdown("""
        - **What:** Stars, forks, and activity metrics for key data/AI repositories
        - **Volume:** 81 curated repositories
        - **Source:** GitHub REST API
        - **Selection criteria:** Minimum 1,000 stars, relevance to data engineering/AI ecosystem
        - **Categories:** Orchestration, transformation, warehouses, streaming, ML frameworks, etc.
        """)

        st.markdown("### LLM Skill Extractions")
        st.markdown("""
        - **What:** Structured technology/role extraction from job posting text
        - **Volume:** 10,000 posts processed (sample of HN data)
        - **Model:** Claude 3 Haiku
        - **Success rate:** 98.2% (182 failures due to JSON truncation)
        - **Cost:** ~$4.50 total ($0.00045/post)
        """)

    with tab2:
        st.subheader("Data Pipeline")

        st.markdown("""
        ```
        HuggingFace (HN) ─┐
        Kaggle (LinkedIn) ┼──▶ Snowflake Raw ──▶ dbt Staging ──▶ dbt Intermediate ──▶ dbt Marts
        GitHub API ───────┘         │                 │                  │                  │
                                    │                 │                  │                  │
                                    │           (1:1 clean)    (skill extraction)    (facts & dims)
                                    │
                                    ▼
                            ┌───────────────┐
                            │  LLM Layer    │
                            │  (Claude API) │
                            └───────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
           LLM Skill Extraction            Weekly Insights
           (10K sample → 63K mentions)     (Automated reports)
        ```
        """)

        st.markdown("### Tech Stack")
        st.markdown("""
        | Component | Technology |
        |-----------|------------|
        | **Warehouse** | Snowflake |
        | **Transformation** | dbt (21 models, 3 seeds) |
        | **Orchestration** | Airflow |
        | **LLM** | Claude API (Anthropic) |
        | **Visualization** | Streamlit |
        """)

        st.markdown("### dbt Model Layers")
        st.markdown("""
        | Layer | Models | Description |
        |-------|--------|-------------|
        | **Staging** | 6 views | 1:1 with raw sources, light cleaning (strip HTML, parse dates) |
        | **Intermediate** | 4 tables | Business logic - keyword extraction via CROSS JOIN + CONTAINS |
        | **Marts** | 11 models | Analytics-ready facts and dimensions |
        | **Seeds** | 3 CSVs | Taxonomy reference data (309 rows total) |
        """)

    with tab3:
        st.subheader("Skill Extraction Methods")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Regex (Keyword Matching)")
            st.markdown("""
            **How it works:**
            1. Curated taxonomy of 152 technologies stored in seed CSVs
            2. CROSS JOIN job postings with taxonomy keywords
            3. CONTAINS() function matches keywords in post text
            4. Map keyword variations to canonical names

            **Example mappings:**
            - `postgres`, `postgresql`, `psql` → **PostgreSQL**
            - `k8s`, `kubernetes` → **Kubernetes**
            - `tf`, `terraform` → **Terraform**

            **Pros:** Fast, free, deterministic, runs on full dataset

            **Cons:** Limited to curated taxonomy, misses variations, false positives on common words
            """)

        with col2:
            st.markdown("### LLM (Claude Haiku)")
            st.markdown("""
            **How it works:**
            1. Send job posting text to Claude Haiku
            2. Prompt asks for structured JSON with technologies/roles
            3. Parse JSON response, store in Snowflake
            4. Join back to posting metadata

            **Output format:**
            ```json
            {
              "technologies": [
                {"name": "Python", "category": "language", "confidence": 0.95},
                {"name": "Airflow", "category": "orchestration", "confidence": 0.90}
              ],
              "roles": [...]
            }
            ```

            **Pros:** Handles variations automatically, discovers new technologies, higher recall

            **Cons:** Costs money, slower, slight variation between runs
            """)

        st.divider()

        st.markdown("### Comparison Results")
        st.markdown("""
        | Metric | LLM | Regex |
        |--------|-----|-------|
        | Unique technologies | 4,569 | 152 |
        | Avg techs/post | 6.4 | 1.5 |
        | Cost per post | $0.00045 | $0 |
        | Processing time (10K) | ~25 min | Instant |

        **Key finding:** PostgreSQL has 66% agreement between methods (highest). Technologies with unique names agree more; common words like "rust" have more regex false positives.
        """)

    with tab4:
        st.subheader("Technology Taxonomy")

        st.markdown("### Categories")

        categories = {
            "Orchestration": "Airflow, Dagster, Prefect, Mage, Luigi",
            "Transformation": "dbt, Spark, pandas, Polars",
            "Warehouses": "Snowflake, BigQuery, Redshift, Databricks",
            "Streaming": "Kafka, Flink, Kinesis, Spark Streaming",
            "Storage": "S3, GCS, Delta Lake, Iceberg",
            "ETL/ELT": "Fivetran, Airbyte, Stitch, AWS Glue",
            "BI Tools": "Tableau, Looker, Power BI, Metabase",
            "ML Frameworks": "PyTorch, TensorFlow, scikit-learn, XGBoost",
            "LLM/AI": "OpenAI, Claude, Llama, LangChain",
            "Databases": "PostgreSQL, MySQL, MongoDB, Redis"
        }

        for cat, examples in categories.items():
            st.markdown(f"**{cat}:** {examples}")

        st.divider()

        st.subheader("Role Taxonomy")

        st.markdown("""
        | Tier | Roles |
        |------|-------|
        | **Tier 1: Core** | Data Engineer, Analytics Engineer, Data Analyst, Data Scientist |
        | **Tier 2: Adjacent** | ML Engineer, MLOps Engineer, Platform Engineer, BI Engineer |
        | **Tier 3: Overlapping** | Backend Engineer (data focus), AI Engineer, SRE (data infra) |
        """)

        st.markdown("### Data Eras")
        st.markdown("""
        - **Pre-2015:** Hadoop Era
        - **2015-2019:** Cloud Transition
        - **2020-2022:** Modern Data Stack
        - **2023+:** AI/LLM Era
        """)

    with tab5:
        st.subheader("Known Limitations")

        st.warning("""
        **HN data skews toward startups and tech-native companies.**
        Enterprise/Fortune 500 hiring patterns may differ significantly. This data represents what's hot in the startup/VC-backed ecosystem, not necessarily the broader market.
        """)

        st.warning("""
        **LinkedIn data is a single cross-sectional snapshot (January 2024).**
        No time-series analysis is possible. Trend claims are based on HN data only.
        """)

        st.warning("""
        **Regex extraction is taxonomy-limited.**
        Only detects 152 curated technologies. The LLM found 4,569 unique technologies, meaning regex misses ~97% of the technology diversity.
        """)

        st.warning("""
        **LLM extraction covers only 10K posts (11% sample).**
        Full 93K dataset uses regex for cost efficiency. LLM results may not fully generalize.
        """)

        st.info("""
        **Skill extraction uses keyword matching, which has known issues:**
        - May miss context-dependent mentions
        - Can capture false positives (e.g., "rust" the oxidation vs Rust the language)
        - Doesn't understand negations ("we don't use X")
        """)

        st.markdown("### Licensing")
        st.markdown("""
        - **LinkedIn dataset:** Used under Kaggle's terms for academic/research purposes only
        - **HN data:** Public via HuggingFace and HN Firebase API
        - **GitHub data:** Accessed via public REST API
        """)


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    """Main app entry point."""

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Executive Summary", "Technology Trends", "Role Trends", "GitHub & LinkedIn", "LLM vs Regex", "Data Explorer", "Methodology"]
    )

    # Year range filter (for trend pages)
    st.sidebar.divider()
    st.sidebar.header("Filters")
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=2011,
        max_value=2025,
        value=(2018, 2025)
    )

    # About section
    st.sidebar.divider()
    st.sidebar.markdown("### About")
    st.sidebar.markdown(
        "Tracking technology and role trends across the data/AI ecosystem using HN job postings, LinkedIn skills, and GitHub activity."
    )
    st.sidebar.markdown("**Data sources:**")
    st.sidebar.markdown("- HN Who Is Hiring (93K+ posts)")
    st.sidebar.markdown("- LinkedIn Jobs (1.3M snapshot)")
    st.sidebar.markdown("- GitHub Repos (81 tracked)")
    st.sidebar.markdown("- LLM Extraction (10K sample)")

    st.sidebar.divider()
    st.sidebar.caption("Streamlit + dbt + Snowflake + Claude")

    # Render selected page
    if page == "Executive Summary":
        render_executive_summary()
    elif page == "Technology Trends":
        render_technology_trends(year_range)
    elif page == "Role Trends":
        render_role_trends(year_range)
    elif page == "GitHub & LinkedIn":
        render_github_linkedin()
    elif page == "LLM vs Regex":
        render_llm_analysis()
    elif page == "Data Explorer":
        render_data_explorer()
    elif page == "Methodology":
        render_methodology()


if __name__ == "__main__":
    main()
