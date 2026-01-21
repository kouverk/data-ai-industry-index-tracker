
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select posting_id
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_linkedin__skills_standardized
where posting_id is null



  
  
      
    ) dbt_internal_test