
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select skill_name
from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_intermediate.int_linkedin__skills_standardized
where skill_name is null



  
  
      
    ) dbt_internal_test