
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select database_name
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_hn__databases_extracted
where database_name is null



  
  
      
    ) dbt_internal_test