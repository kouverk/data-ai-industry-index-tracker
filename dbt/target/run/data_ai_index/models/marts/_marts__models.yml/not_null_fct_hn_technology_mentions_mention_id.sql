
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select mention_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_hn_technology_mentions
where mention_id is null



  
  
      
    ) dbt_internal_test