SELECT
    c.name,
    ms.volume_24h
from market_snapshots ms

join coins c
    on c.coin_id = ms.coin_id

where ms.volume_24h is not null and ms.collection_time = (
    select MAX(collection_time)
    from market_snapshots
)
order by  ms.volume_24h DESC;