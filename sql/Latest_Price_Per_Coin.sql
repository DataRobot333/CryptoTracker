SELECT DISTINCT ON (c.symbol)
    c.symbol,
    p.price_usd,
    p.collected_at
FROM price_snapshots p
JOIN coins c ON c.coin_id = p.coin_id
ORDER BY c.symbol, p.collected_at DESC;