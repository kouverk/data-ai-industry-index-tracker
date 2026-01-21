
    
    

select
    posting_id as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__postings
where posting_id is not null
group by posting_id
having count(*) > 1


