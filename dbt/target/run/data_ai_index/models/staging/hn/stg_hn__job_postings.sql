
  create or replace   view DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_hn__job_postings
  
  
  
  
  as (
    with source as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.raw_hn_job_postings
),

cleaned as (
    select
        id as posting_id,
        thread_id,
        thread_month,
        author,

        -- Clean HTML from text
        regexp_replace(text, '<[^>]+>', ' ') as posting_text,

        -- Parse month into proper date
        to_date(thread_month, 'MMMM YYYY') as posting_month,
        extract(year from to_date(thread_month, 'MMMM YYYY')) as posting_year,

        posted_at,
        _loaded_at

    from source
    where text is not null
      and trim(text) != ''
)

select * from cleaned
  );

