SELECT
    c.name,
    round(
        ms.volume_24h/ NULLIF(ms.market_cap,0),
        4
    ) as vol_mc_ratio
from market_snapshots ms

join coins c
    on c.coin_id = ms.coin_id

WHERE ms.volume_24h/ NULLIF(ms.market_cap,0) is not null and
    ms.collection_time = (
        select MAX(collection_time)
        from market_snapshots
    )

ORDER BY vol_mc_ratio DESC;