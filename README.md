# E-commerce SQL Analytics

Answering real business questions about an online store **with SQL**, against a
normalised SQLite database. The focus is on writing clean, correct analytical SQL —
JOINs, CTEs, window functions and aggregation — not on Python.

## Database schema

A small star schema, built and populated by [`data/build_db.py`](data/build_db.py):

```
customers   (customer_id PK, name, country, signup_date)        400 rows
products    (product_id PK, product_name, category, price)       60 rows
orders      (order_id PK, customer_id FK, order_date, status)  3,000 rows
order_items (order_item_id PK, order_id FK, product_id FK, …)  7,400+ rows
```

Foreign keys and indexes (`idx_orders_customer`, `idx_items_order`,
`idx_items_product`) are defined in the build script.

## Business questions answered

| # | Question | SQL features |
|---|----------|--------------|
| 1 | Monthly revenue trend | JOIN, GROUP BY, date bucketing |
| 2 | Most valuable customers | CTE + `RANK() OVER` |
| 3 | Category performance & share | `SUM() OVER ()` for % of total |
| 4 | Revenue & AOV by country | JOIN chain, derived metrics |
| 5 | Repeat-purchase rate | conditional aggregation |
| 6 | Cumulative revenue | running `SUM() OVER (ORDER BY …)` |

Each lives as a standalone file in [`sql/`](sql); the notebook runs them and
visualises the answers.

## What's inside

```
ecommerce-sql-analytics/
├── data/
│   ├── build_db.py          # creates schema + seeds synthetic data
│   └── ecommerce.db         # SQLite database (generated)
├── sql/                     # 6 documented, reusable analytical queries
├── notebooks/
│   └── sql_analysis.ipynb   # runs the queries + charts the results
└── requirements.txt
```

## Run it

```bash
pip install -r requirements.txt
python data/build_db.py                 # (re)build the database
jupyter notebook notebooks/sql_analysis.ipynb

# or run a query straight from the CLI:
sqlite3 data/ecommerce.db < sql/02_top_customers.sql
```

---
Part of my [data & ML portfolio](https://github.com/ABouns).
