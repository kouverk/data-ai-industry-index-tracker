
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select role_name
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_marts.dim_roles
where role_name is null



  
  
      
    ) dbt_internal_test