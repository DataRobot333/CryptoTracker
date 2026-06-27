SELECT
    c.name,
    AVG(ms.volume_24h) as average_vol
FROM market_snapshots ms

join coins c
    on c.coin_id = ms.coin_id
where ms.volume_24h is not null
GROUP BY c.name;