with role_extracted as (
    select * from {{ ref('int_hn__roles_extracted') }}
),

dim_roles as (
    select * from {{ ref('dim_roles') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['r.posting_id', 'r.role']) }} as mention_id,
    r.posting_id,
    dr.role_id,
    r.role as role_name,
    r.tier,
    r.posting_month,
    r.posting_year
from role_extracted r
left join dim_roles dr on r.role = dr.role_name
