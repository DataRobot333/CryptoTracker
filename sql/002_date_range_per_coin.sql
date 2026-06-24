SELECT
    c.symbol,
    count(p.*) AS data_points,
    MIN(p.collected_at) AS start_time,
    MAX(p.collected_at) AS end_time
FROM price_snapshots p
JOIN coins c ON c.coin_id = p.coin_id
GROUP BY c.symbol;