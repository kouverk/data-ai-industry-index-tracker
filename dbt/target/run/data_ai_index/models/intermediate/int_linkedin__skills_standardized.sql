
  
    

create or replace transient table DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_linkedin__skills_standardized
    
    
    
    as (

with skills as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__skills
),

tech_mappings as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.technology_mappings
),

-- Try to match LinkedIn skills to our technology taxonomy
matched as (
    select
        s.posting_id,
        s.skill_name as original_skill,
        t.canonical_name as technology,
        t.category,
        t.era
    from skills s
    left join tech_mappings t
        on lower(s.skill_name) = lower(t.keyword)
)

select
    posting_id,
    original_skill,
    coalesce(technology, original_skill) as skill_name,
    coalesce(category, 'other') as category,
    coalesce(era, 'unknown') as era,
    case when technology is not null then true else false end as is_standardized
from matched
    )
;


  