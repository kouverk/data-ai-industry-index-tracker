
  create or replace   view DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__skills
  
  
  
  
  as (
    with source as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.raw_linkedin_skills
),

-- Split comma-separated skills into individual rows
exploded as (
    select
        job_link as posting_id,
        trim(s.value::string) as skill_name,
        _loaded_at
    from source,
    lateral flatten(input => split(job_skills, ',')) as s
    where job_skills is not null
      and trim(job_skills) != ''
)

select * from exploded
where skill_name is not null
  and skill_name != ''
  );

