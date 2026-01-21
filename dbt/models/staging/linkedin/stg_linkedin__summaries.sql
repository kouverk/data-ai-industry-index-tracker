with source as (
    select * from {{ source('raw', 'raw_linkedin_summaries') }}
),

cleaned as (
    select
        job_link as posting_id,
        job_summary as description_text,
        _loaded_at
    from source
    where job_summary is not null
      and trim(job_summary) != ''
)

select * from cleaned
