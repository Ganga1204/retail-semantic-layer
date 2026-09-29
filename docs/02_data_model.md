# Step 4: Data Model Architecture

The repository follows standard Medallion architecture (Bronze -> Silver -> Gold) stored within DuckDB.

## Layer Summary

| Layer | Source / Model | Materialization | Description |
| :--- | :--- | :--- | :--- |
| **Bronze** | `seeds/*.csv` | Seed tables | Raw ingested synthetic transaction data. |
| **Silver** | `stg_customers`, `stg_orders`, `stg_tickets` | Views | Cleansed, strongly typed staging layer. |
| **Gold** | `dim_customer`, `fct_orders`, `fct_tickets` | Tables | Governed dimensional marts for analytical consumption. |

## Gold Layer Mart Specifications

| Table | Grain | Purpose & Key Columns |
| :--- | :--- | :--- |
| `dim_customer` | 1 row per `customer_id` | Customer profile dimension containing demographic attributes and pre-calculated activity flags (`is_active_90d`, `is_active_365d`, `is_active_30d_support`). |
| `fct_orders` | 1 row per `order_id` | Fact table recording purchase amounts, transaction timestamps, and order lifecycle statuses (`completed`, `refunded`, `cancelled`). |
| `fct_tickets` | 1 row per `ticket_id` | Fact table capturing customer support interactions, ticket dates, and issue categories (`billing`, `delivery`, `product`, `other`). |
