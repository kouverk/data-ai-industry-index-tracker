
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select posting_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.fct_hn_role_mentions
where posting_id is null



  
  
      
    ) dbt_internal_test