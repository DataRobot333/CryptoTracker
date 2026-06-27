-- quick solution
--select pg_size_pretty(pg_database_size(current_database()));

--more detailed solution
SELECT
    relname as table_name,
    n_live_tup as estimated_rows,
    pg_size_pretty(pg_relation_size(relid)) as table_size,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size

from pg_catalog.pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC;