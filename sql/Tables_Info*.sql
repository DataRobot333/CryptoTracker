SELECT count(*) AS "number of rows" From coins
UNION SELECT count(*) FROM price_snapshots;