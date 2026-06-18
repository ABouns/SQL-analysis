"""Build a small normalised e-commerce SQLite database for SQL analytics.

Schema (star-ish, 4 tables)
    customers(customer_id PK, name, country, signup_date)
    products(product_id PK, product_name, category, price)
    orders(order_id PK, customer_id FK, order_date, status)
    order_items(order_item_id PK, order_id FK, product_id FK, quantity, unit_price)

Run:  python data/build_db.py   ->  data/ecommerce.db
"""

import sqlite3
import numpy as np
import pandas as pd

RNG = np.random.default_rng(123)
DB = "data/ecommerce.db"

SCHEMA = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id  INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    country      TEXT NOT NULL,
    signup_date  TEXT NOT NULL
);
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    price        REAL NOT NULL
);
CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date  TEXT NOT NULL,
    status      TEXT NOT NULL
);
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL REFERENCES orders(order_id),
    product_id    INTEGER NOT NULL REFERENCES products(product_id),
    quantity      INTEGER NOT NULL,
    unit_price    REAL NOT NULL
);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_items_order ON order_items(order_id);
CREATE INDEX idx_items_product ON order_items(product_id);
"""

COUNTRIES = ["Belgium", "France", "Germany", "Netherlands", "Spain", "Italy"]
CATS = {
    "Electronics": (50, 600),
    "Home": (10, 120),
    "Books": (5, 40),
    "Sports": (15, 200),
    "Beauty": (8, 80),
}
FIRST = ["Emma", "Liam", "Noah", "Olivia", "Lucas", "Mia", "Leon", "Sofia",
         "Hugo", "Julia", "Adam", "Lena", "Tom", "Anna", "Max", "Sara"]
LAST = ["Peeters", "Janssens", "Martin", "Müller", "De Smet", "Garcia",
        "Rossi", "Dubois", "Wouters", "Bernard"]


def build_frames():
    n_cust, n_prod, n_orders = 400, 60, 3000

    customers = pd.DataFrame({
        "customer_id": np.arange(1, n_cust + 1),
        "name": [f"{RNG.choice(FIRST)} {RNG.choice(LAST)}" for _ in range(n_cust)],
        "country": RNG.choice(COUNTRIES, n_cust,
                              p=[0.30, 0.20, 0.18, 0.14, 0.10, 0.08]),
        "signup_date": (pd.to_datetime("2022-01-01")
                        + pd.to_timedelta(RNG.integers(0, 900, n_cust), "D")
                        ).strftime("%Y-%m-%d"),
    })

    cats = list(CATS)
    prod_cat = RNG.choice(cats, n_prod)
    prices = [round(RNG.uniform(*CATS[c]), 2) for c in prod_cat]
    products = pd.DataFrame({
        "product_id": np.arange(1, n_prod + 1),
        "product_name": [f"{c} Item {i}" for i, c in enumerate(prod_cat, 1)],
        "category": prod_cat,
        "price": prices,
    })

    # weight repeat customers so RFM-style questions are meaningful
    cust_weights = RNG.gamma(2.0, 1.0, n_cust)
    cust_weights /= cust_weights.sum()
    orders = pd.DataFrame({
        "order_id": np.arange(1, n_orders + 1),
        "customer_id": RNG.choice(customers.customer_id, n_orders, p=cust_weights),
        "order_date": (pd.to_datetime("2023-01-01")
                       + pd.to_timedelta(RNG.integers(0, 730, n_orders), "D")
                       ).strftime("%Y-%m-%d"),
        "status": RNG.choice(["completed", "returned", "cancelled"],
                             n_orders, p=[0.86, 0.09, 0.05]),
    })

    # 1-4 line items per order
    rows = []
    item_id = 1
    for oid in orders.order_id:
        for _ in range(int(RNG.integers(1, 5))):
            pid = int(RNG.integers(1, n_prod + 1))
            price = float(products.loc[products.product_id == pid, "price"].iloc[0])
            rows.append((item_id, oid, pid, int(RNG.integers(1, 4)), price))
            item_id += 1
    order_items = pd.DataFrame(
        rows, columns=["order_item_id", "order_id", "product_id",
                       "quantity", "unit_price"])

    return customers, products, orders, order_items


def main():
    customers, products, orders, order_items = build_frames()
    conn = sqlite3.connect(DB)
    conn.executescript(SCHEMA)
    customers.to_sql("customers", conn, if_exists="append", index=False)
    products.to_sql("products", conn, if_exists="append", index=False)
    orders.to_sql("orders", conn, if_exists="append", index=False)
    order_items.to_sql("order_items", conn, if_exists="append", index=False)
    conn.commit()
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ["customers", "products", "orders", "order_items"]}
    conn.close()
    print(f"Built {DB}")
    for t, n in counts.items():
        print(f"  {t:>12}: {n} rows")


if __name__ == "__main__":
    main()
