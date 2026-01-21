
  create or replace   view DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_github__repo_stats
  
  
  
  
  as (
    with source as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.raw_github_repo_stats
),

cleaned as (
    select
        full_name as repo_id,
        repo_name,
        full_name,
        category,
        stars,
        forks,
        open_issues,
        watchers,
        language as primary_language,
        description,
        created_at as repo_created_at,
        updated_at as repo_updated_at,
        pushed_at as last_push_at,
        fetched_at,
        _loaded_at

    from source
)

select * from cleaned
  );

