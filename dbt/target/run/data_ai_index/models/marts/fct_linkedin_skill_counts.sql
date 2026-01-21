
  
    

create or replace transient table DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts
    
    
    
    as (with skills as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_linkedin__skills_standardized
),

postings as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__postings
)

select
    s.skill_name,
    s.category,
    s.era,
    s.is_standardized,
    count(distinct s.posting_id) as job_count,
    count(distinct s.posting_id) * 100.0 / (select count(distinct posting_id) from postings) as pct_of_jobs
from skills s
group by 1, 2, 3, 4
order by job_count desc
    )
;


  