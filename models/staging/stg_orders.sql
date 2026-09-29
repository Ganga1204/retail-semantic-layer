select
    cast(order_id as integer)     as order_id,
    cast(customer_id as integer)  as customer_id,
    cast(order_date as date)      as order_date,
    cast(amount as double)        as amount,
    lower(status)                 as status
from {{ ref('orders') }}
