
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select role_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_roles
where role_id is null



  
  
      
    ) dbt_internal_test