with repo_stats as (
    select * from DATAEXPERT_STUDENT.KOUVERK_DATA_INDUSTRY_staging.stg_github__repo_stats
)

select
    repo_id,
    repo_name,
    full_name,
    category,
    primary_language,
    description,
    stars,
    forks,
    open_issues,
    watchers,
    repo_created_at,
    last_push_at,
    fetched_at,
    -- Derived metrics
    round(forks * 1.0 / nullif(stars, 0), 4) as fork_to_star_ratio,
    round(open_issues * 1.0 / nullif(stars, 0), 6) as issues_per_star,
    datediff('day', repo_created_at::date, fetched_at::date) as days_since_creation,
    datediff('day', last_push_at::date, fetched_at::date) as days_since_last_push,
    -- Activity classification
    case
        when datediff('day', last_push_at::date, fetched_at::date) <= 7 then 'Very Active'
        when datediff('day', last_push_at::date, fetched_at::date) <= 30 then 'Active'
        when datediff('day', last_push_at::date, fetched_at::date) <= 90 then 'Moderate'
        else 'Low Activity'
    end as activity_level
from repo_stats