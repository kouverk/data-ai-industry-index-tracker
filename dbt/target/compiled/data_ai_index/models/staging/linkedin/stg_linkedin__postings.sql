with source as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY.raw_linkedin_postings
),

cleaned as (
    select
        job_link as posting_id,
        job_title,
        company,
        job_location,

        -- Parse location into components
        split_part(job_location, ',', 1) as city,
        trim(split_part(job_location, ',', 2)) as state_or_country,

        first_seen as posted_at,
        job_level,
        job_type,
        search_city,
        search_country,
        search_position,

        _loaded_at

    from source
    where job_title is not null
)

select * from cleaned