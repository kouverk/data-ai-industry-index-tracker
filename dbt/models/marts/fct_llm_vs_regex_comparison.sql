{{
    config(
        materialized='table'
    )
}}

with llm_mentions as (
    select
        posting_id,
        technology_name,
        llm_category as category,
        confidence
    from {{ ref('fct_llm_technology_mentions') }}
),

regex_mentions as (
    select
        posting_id,
        technology_name,
        category
    from {{ ref('fct_hn_technology_mentions') }}
),

-- Get the set of postings that both methods processed
llm_postings as (
    select distinct posting_id
    from {{ ref('stg_llm__skill_extractions') }}
    where is_successful
),

-- Only compare on overlapping postings
regex_on_llm_posts as (
    select r.*
    from regex_mentions r
    inner join llm_postings lp on r.posting_id::varchar = lp.posting_id::varchar
),

-- Full outer join to see what each method found
comparison as (
    select
        coalesce(l.posting_id, r.posting_id) as posting_id,
        coalesce(l.technology_name, r.technology_name) as technology_name,
        l.technology_name is not null as found_by_llm,
        r.technology_name is not null as found_by_regex,
        l.confidence as llm_confidence,
        coalesce(l.category, r.category) as category,
        case
            when l.technology_name is not null and r.technology_name is not null then 'both'
            when l.technology_name is not null then 'llm_only'
            else 'regex_only'
        end as detection_method
    from llm_mentions l
    full outer join regex_on_llm_posts r
        on l.posting_id::varchar = r.posting_id::varchar
        and lower(l.technology_name) = lower(r.technology_name)
),

-- Aggregate by technology (use lower for consistent grouping)
tech_summary as (
    select
        lower(technology_name) as technology_name_lower,
        min(technology_name) as technology_name,
        min(category) as category,
        count(distinct posting_id) as total_postings,
        count(distinct case when found_by_llm then posting_id end) as llm_count,
        count(distinct case when found_by_regex then posting_id end) as regex_count,
        count(distinct case when detection_method = 'both' then posting_id end) as both_count,
        count(distinct case when detection_method = 'llm_only' then posting_id end) as llm_only_count,
        count(distinct case when detection_method = 'regex_only' then posting_id end) as regex_only_count,
        avg(case when found_by_llm then llm_confidence end) as avg_llm_confidence
    from comparison
    group by 1
)

select
    technology_name,
    category,
    total_postings,
    llm_count,
    regex_count,
    both_count,
    llm_only_count,
    regex_only_count,
    round(avg_llm_confidence, 3) as avg_llm_confidence,
    round(both_count * 100.0 / nullif(greatest(llm_count, regex_count), 0), 1) as agreement_pct,
    round(llm_only_count * 100.0 / nullif(llm_count, 0), 1) as llm_unique_pct,
    round(regex_only_count * 100.0 / nullif(regex_count, 0), 1) as regex_unique_pct
from tech_summary
where total_postings >= 5
order by total_postings desc
