import os
import random
from datetime import date, timedelta
import pandas as pd
from faker import Faker

random.seed(7)
Faker.seed(7)
fake = Faker()

START, END = date(2025, 7, 1), date(2026, 6, 30)   # matches as_of_date

customers, orders, tickets = [], [], []
oid = tid = 1

for cid in range(1, 1001):
    signup = fake.date_between(date(2024, 7, 1), date(2026, 5, 31))
    customers.append(dict(
        customer_id=cid,
        full_name=fake.name(),
        country=random.choice(["US", "UK", "IN", "DE", "CA"]),
        segment=random.choice(["consumer", "small_business", "enterprise"]),
        signup_date=signup
    ))
    lo = max(signup, START)
    num_orders = random.choices([0, 1, 2, 4, 8], [15, 25, 25, 20, 15])[0]
    for _ in range(num_orders):
        d = lo + timedelta(days=random.randint(0, (END - lo).days))
        orders.append(dict(
            order_id=oid,
            customer_id=cid,
            order_date=d,
            amount=round(random.lognormvariate(4, 0.7), 2),
            status=random.choices(["completed", "refunded", "cancelled"], [92, 5, 3])[0]
        ))
        oid += 1

    if random.random() < 0.3:
        d = lo + timedelta(days=random.randint(0, (END - lo).days))
        tickets.append(dict(
            ticket_id=tid,
            customer_id=cid,
            opened_date=d,
            category=random.choice(["billing", "delivery", "product", "other"])
        ))
        tid += 1

os.makedirs("seeds", exist_ok=True)

for name, rows in [("customers", customers), ("orders", orders), ("tickets", tickets)]:
    pd.DataFrame(rows).to_csv(f"seeds/{name}.csv", index=False)

print(f"Generated {len(customers)} customers, {len(orders)} orders, {len(tickets)} tickets successfully in seeds/")
