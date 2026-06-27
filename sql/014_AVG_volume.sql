with avg_vol as (
    SELECT
        coin_id,
        avg(volume_24h)
    from market_snapshots
    GROUP BY coin_id
)

select *
from avg_vol;