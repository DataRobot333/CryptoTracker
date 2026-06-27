with latest as (
    SELECT
        *
    from market_snapshots
    WHERE collection_time = (
        SELECT Max(collection_time)
        from market_snapshots
    )
)
select *
from latest;