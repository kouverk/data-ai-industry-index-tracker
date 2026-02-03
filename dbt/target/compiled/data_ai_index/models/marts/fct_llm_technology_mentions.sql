with extractions as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_llm__skill_extractions
    where is_successful
),

postings as (
    select
        posting_id,
        posting_month,
        posting_year
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
),

-- Flatten the technologies VARIANT array into rows
flattened_tech as (
    select
        e.posting_id,
        f.value:name::varchar as technology_name,
        f.value:category::varchar as category,
        f.value:confidence::float as confidence
    from extractions e,
    lateral flatten(input => e.technologies) f
),

-- Deduplicate: same posting + technology, keep highest confidence
deduped as (
    select *
    from flattened_tech
    qualify row_number() over (
        partition by posting_id, lower(technology_name)
        order by confidence desc
    ) = 1
),

dim_tech as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_technologies
)

select
    md5(cast(coalesce(cast(d.posting_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(d.technology_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as mention_id,
    d.posting_id,
    dt.technology_id,
    d.technology_name,
    d.category as llm_category,
    dt.category as taxonomy_category,
    d.confidence,
    p.posting_month,
    p.posting_year,
    'llm' as extraction_method
from deduped d
inner join postings p on d.posting_id::varchar = p.posting_id::varchar
left join dim_tech dt on lower(d.technology_name) = lower(dt.technology_name)
where d.technology_name is not null