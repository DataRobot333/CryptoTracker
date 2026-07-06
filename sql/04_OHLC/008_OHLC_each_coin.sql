with daily_stat as (
SELECT
    coin_id,
    DATE(collection_time) as trade_day,
    MIN(collection_time) as first_time,
    MAX(collection_time) as last_time,
    max(price_usd) as high_price,
    MIN(price_usd) as low_price
from market_snapshots
GROUP BY coin_id, DATE(collection_time)
)

SELECT
    ds.coin_id,
    open_ms.price_usd as open_price,
    ds.high_price,
    ds.low_price,
    close_ms.price_usd as close_price

from daily_stat as ds

JOIN market_snapshots open_ms
    on open_ms.coin_id = ds.coin_id
    and open_ms.collection_time = ds.first_time

JOIN market_snapshots close_ms
    on close_ms.coin_id = ds.coin_id
    and close_ms.collection_time = ds.last_time

ORDER BY ds.trade_day DESC, ds.coin_id;SELECT
    c.name,
    DATE(ms.collection_time),
    MAX(ms.collection_time)
    

from market_snapshots ms
join coins c
    on c.coin_id = ms.coin_id
GROUP BY c.name, date(ms.collection_time)

;