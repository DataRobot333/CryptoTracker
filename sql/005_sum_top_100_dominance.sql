select 
    round(sum(market_cap_dominance), 2) as top_100_dominance
from market_snapshots
where collection_time = (select max(collection_time) from market_snapshots)
    and cmc_rank <= 100

;