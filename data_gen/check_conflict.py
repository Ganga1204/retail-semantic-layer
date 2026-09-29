import duckdb
import pandas as pd

con = duckdb.connect("retail.duckdb")
df = con.execute("""
    select 
        sum(is_active_90d) as active_marketing_90d, 
        sum(is_active_365d) as active_finance_365d, 
        sum(is_active_30d_support) as active_support_30d 
    from dim_customer
""").df()

print("==========================================================================")
print("  Raw Data Model Conflicting Counts (The Headline Business Problem)")
print("==========================================================================")
print(df.to_string(index=False))
print("==========================================================================")
