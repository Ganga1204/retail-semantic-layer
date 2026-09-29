select
    ticket_id,
    customer_id,
    opened_date,
    category
from {{ ref('stg_tickets') }}
