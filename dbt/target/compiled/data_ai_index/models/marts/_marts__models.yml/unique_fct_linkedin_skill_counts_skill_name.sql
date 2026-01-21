
    
    

select
    skill_name as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_linkedin_skill_counts
where skill_name is not null
group by skill_name
having count(*) > 1


