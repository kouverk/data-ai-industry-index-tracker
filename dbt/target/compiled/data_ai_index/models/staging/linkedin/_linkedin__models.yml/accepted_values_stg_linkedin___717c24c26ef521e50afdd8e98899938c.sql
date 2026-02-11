
    
    

with all_values as (

    select
        job_level as value_field,
        count(*) as n_records

    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__postings
    group by job_level

)

select *
from all_values
where value_field not in (
    'Entry level','Mid-Senior level','Director','Executive','Associate','Internship','Not Applicable'
)


