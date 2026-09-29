select
    cast(ticket_id as integer)    as ticket_id,
    cast(customer_id as integer)  as customer_id,
    cast(opened_date as date)     as opened_date,
    cast(category as varchar)     as category
from {{ ref('tickets') }}
