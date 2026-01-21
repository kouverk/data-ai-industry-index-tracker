
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    mention_id as unique_field,
    count(*) as n_records

from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_hn_role_mentions
where mention_id is not null
group by mention_id
having count(*) > 1



  
  
      
    ) dbt_internal_test