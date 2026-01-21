
    
    

select
    technology_id as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_technologies
where technology_id is not null
group by technology_id
having count(*) > 1


