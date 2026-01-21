
    
    

select
    mention_id as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions
where mention_id is not null
group by mention_id
having count(*) > 1


