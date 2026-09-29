with completed as (
    select customer_id,
           max(order_date) as last_order_date,
           count(*)        as completed_orders,
           sum(amount)     as lifetime_revenue
    from {{ ref('stg_orders') }}
    where status = 'completed'
    group by 1
),
tix as (
    select customer_id, max(opened_date) as last_ticket_date
    from {{ ref('stg_tickets') }}
    group by 1
)
select
    c.customer_id, c.full_name, c.country, c.segment, c.signup_date,
    o.last_order_date,
    coalesce(o.completed_orders, 0)  as completed_orders,
    coalesce(o.lifetime_revenue, 0)  as lifetime_revenue,
    cast(coalesce(date_diff('day', o.last_order_date, date '{{ var("as_of_date") }}') <= 90,  false) as integer) as is_active_90d,
    cast(coalesce(date_diff('day', o.last_order_date, date '{{ var("as_of_date") }}') <= 365, false) as integer) as is_active_365d,
    cast(coalesce(
        date_diff('day', o.last_order_date,  date '{{ var("as_of_date") }}') <= 30 or
        date_diff('day', t.last_ticket_date, date '{{ var("as_of_date") }}') <= 30, false) as integer) as is_active_30d_support
from {{ ref('stg_customers') }} c
left join completed o using (customer_id)
left join tix t using (customer_id)
