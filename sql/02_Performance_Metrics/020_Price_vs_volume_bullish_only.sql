with latest as (
    SELECT
        *
    from market_snapshots
    where collection_time = (
        SELECT MAX(collection_time)
        from market_snapshots
    )
),

avg_volume as (
    select
        coin_id,
        AVG(volume_24h) as avg_volume_30d
    from market_snapshots
    GROUP BY coin_id
),

vol_info as (
    select
        c.name,
        l.coin_id,
        l.price_usd,
        l.volume_24h,
        l.precent_change_24h,
        av.avg_volume_30d,

        case
            when av.avg_volume_30d is null or av.avg_volume_30d = 0 then null
            else l.volume_24h / av.avg_volume_30d
        end as volume_spike_ratio

    from latest l
    join coins c on c.coin_id = l.coin_id
    left join avg_volume av on av.coin_id = l.coin_id
),

signals as (
    select 
        *,
        case
            when precent_change_24h > 0 and volume_spike_ratio > 1.5 then 'strong_bullish'
            when precent_change_24h < 0 and volume_spike_ratio < 1.5 then 'strong_bearish'
            when precent_change_24h > 0 and volume_spike_ratio < 1 then 'weak_rally'
            when precent_change_24h < 0 and volume_spike_ratio < 1 then 'weak_sell_off'
            else 'neutral_market'
        end as signal
    from vol_info
)

select
    *

from signals
where signal = 'strong_bullish';