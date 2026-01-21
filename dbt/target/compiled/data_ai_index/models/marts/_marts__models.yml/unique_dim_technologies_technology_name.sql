
    
    

select
    technology_name as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_technologies
where technology_name is not null
group by technology_name
having count(*) > 1


