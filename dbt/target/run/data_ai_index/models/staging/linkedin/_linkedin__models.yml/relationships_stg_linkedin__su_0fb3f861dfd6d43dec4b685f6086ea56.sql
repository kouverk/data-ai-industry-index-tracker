
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with child as (
    select posting_id as from_field
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__summaries
    where posting_id is not null
),

parent as (
    select posting_id as to_field
    from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_linkedin__postings
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null



  
  
      
    ) dbt_internal_test