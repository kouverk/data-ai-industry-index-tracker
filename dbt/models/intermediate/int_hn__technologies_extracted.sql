{{
    config(
        materialized='table'
    )
}}

with postings as (
    select * from {{ ref('stg_hn__job_postings') }}
),

tech_mappings as (
    select * from {{ ref('technology_mappings') }}
),

-- Cross join postings with tech mappings and check for matches
matched as (
    select
        p.posting_id,
        p.posting_month,
        p.posting_year,
        t.canonical_name as technology,
        t.category,
        t.era
    from postings p
    cross join tech_mappings t
    where regexp_like(lower(p.posting_text), '\\b' || lower(t.keyword) || '\\b')
)

select distinct
    posting_id,
    posting_month,
    posting_year,
    technology,
    category,
    era
from matched
