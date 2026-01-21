
    
    

select
    repo_id as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_github_repo_stats
where repo_id is not null
group by repo_id
having count(*) > 1


