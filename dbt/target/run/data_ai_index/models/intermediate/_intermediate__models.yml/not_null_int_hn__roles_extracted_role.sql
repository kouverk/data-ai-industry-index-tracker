
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select role
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_hn__roles_extracted
where role is null



  
  
      
    ) dbt_internal_test