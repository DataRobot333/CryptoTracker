with latest as (
    select *
    from market_snapshots
    WHERE collection_time = (
        select max(collection_time)
        from market_snapshots
    )
),
avg_volume as (
    select
        coin_id,
        AVG(volume_24h) as avg_volume_30d
    from market_snapshots
    GROUP BY coin_id
)
select
    c.name,
    l.coin_id,
    l.price_usd,
    l.volume_24h,
    av.avg_volume_30d,
    l.precent_change_24h,
    case
        when av.avg_volume_30d is null or av.avg_volume_30d = 0 then null
        else l.volume_24h / av.avg_volume_30d
    end as volume_spike_ratio

from latest l
join coins c on c.coin_id = l.coin_id
left join avg_volume av on av.coin_id = l.coin_id;