with avg_vol as (
    SELECT
        coin_id,
        AVG(volume_24h) as avg_vol
    from market_snapshots
    GROUP BY coin_id
)

SELECT
    c.name,
    ms.volume_24h,
    av.avg_vol,
    round(ms.volume_24h/av.avg_vol, 2) as spike_ratio
from market_snapshots ms

join avg_vol av
    on ms.coin_id = av.coin_id

join coins c
    on c.coin_id = ms.coin_id

where ms.collection_time = (
    SELECT 
        MAX(collection_time)
    from market_snapshots
)
and ms.volume_24h > av.avg_vol * 2

ORDER BY spike_ratio desc;