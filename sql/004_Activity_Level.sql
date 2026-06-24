SELECT
    c.name,
    (AVG(ms.volume_24h) / NULLIF(AVG(ms.market_cap), 0) * 100) as vol_mc_ratio,
CASE
    when ((AVG(ms.volume_24h) / NULLIF(AVG(ms.market_cap), 0)) * 100) < 1 THEN 'dormant'
    when (AVG(ms.volume_24h) / NULLIF(AVG(ms.market_cap), 0)) * 100 < 5 THEN 'Low activity'
    when (AVG(ms.volume_24h) / NULLIF(AVG(ms.market_cap), 0)) * 100 < 1 then 'Healthy'
    when (AVG(ms.volume_24h) / NULLIF(AVG(ms.market_cap), 0)) * 100 < 30 then 'active'
    when (AVG(ms.volume_24h) / NULLIF(AVG(ms.market_cap), 0)) * 100 < 60 then 'speculative'
    else 'insuficient data'
END as activity_level

from market_snapshots ms
join coins c
    on c.coin_id = ms.coin_id

GROUP BY c.name

HAVING (AVG(ms.volume_24h) / AVG(ms.market_cap)) is not NULL

ORDER BY vol_mc_ratio DESC

;