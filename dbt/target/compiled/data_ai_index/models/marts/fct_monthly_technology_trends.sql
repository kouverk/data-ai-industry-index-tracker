with mentions as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions
),

postings as (
    select
        posting_month,
        count(distinct posting_id) as total_postings
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
    group by 1
),

monthly_counts as (
    select
        posting_month,
        technology_name,
        category,
        era,
        count(distinct posting_id) as mention_count
    from mentions
    group by 1, 2, 3, 4
)

select
    mc.posting_month,
    mc.technology_name,
    mc.category,
    mc.era,
    mc.mention_count,
    p.total_postings,
    round(mc.mention_count * 100.0 / nullif(p.total_postings, 0), 2) as mention_pct,
    -- Year-over-year comparison
    lag(mc.mention_count, 12) over (
        partition by mc.technology_name
        order by mc.posting_month
    ) as mentions_prev_year,
    -- Month-over-month change
    lag(mc.mention_count, 1) over (
        partition by mc.technology_name
        order by mc.posting_month
    ) as mentions_prev_month
from monthly_counts mc
join postings p on mc.posting_month = p.posting_month