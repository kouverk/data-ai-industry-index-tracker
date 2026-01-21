with role_mappings as (
    select distinct
        canonical_name as role_name,
        tier
    from {{ ref('role_mappings') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['role_name']) }} as role_id,
    role_name,
    tier,
    case tier
        when 1 then 'Core Data Roles'
        when 2 then 'Adjacent Data Roles'
        when 3 then 'AI/ML Specialized'
        when 4 then 'Historical/Legacy'
        when 5 then 'Overlapping Tech'
    end as tier_description,
    current_timestamp() as _created_at
from role_mappings
