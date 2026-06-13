SELECT
count(*) AS total_rows,
MIN(collected_at) as earliest,
MAX(collected_at) as latest
FROM price_snapshots;