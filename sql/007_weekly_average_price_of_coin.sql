select 
    c.name,
    DATE_TRUNC('week', ms.collection_time) as date,
    AVG(ms.price_usd) as avg_price
from market_snapshots ms

join coins c
    on c.coin_id = ms.coin_id

where c.name = 'Dogecoin'

GROUP BY c.name, date

ORDER BY date;