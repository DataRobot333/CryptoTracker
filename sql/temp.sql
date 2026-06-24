select collection_time,
        count(*)
from market_snapshots
GROUP BY collection_time
ORDER BY collection_time DESC
limit 50;