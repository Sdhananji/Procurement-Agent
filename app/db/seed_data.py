import psycopg
from app.config import DATABASE_URL

products = [
    ("SH-001", "Men's Black School Shoes", "school"),
    ("SH-002", "Women's Canvas Sneakers", "casual"),
    ("SH-003", "Kids Velcro Sandals", "kids"),
    ("SH-004", "Men's Leather Formal Shoes", "formal"),
    ("SH-005", "Unisex Rubber Slippers", "casual"),
]
suppliers = [
    ("Lanka Footwear Components", 0.90),
    ("Pacific Sole Traders", 0.75),
    ("Island Leather Works", 0.85),
]
branches = ["Colombo", "Kandy", "Galle"]

with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
    cur.execute("TRUNCATE audit_log, purchase_orders, purchase_requests, "
                "quotations, stock, suppliers, products RESTART IDENTITY CASCADE")
    for sku, name, cat in products:
        cur.execute("INSERT INTO products (sku,name,category) VALUES (%s,%s,%s)", (sku, name, cat))
    for name, rel in suppliers:
        cur.execute("INSERT INTO suppliers (name,reliability_score) VALUES (%s,%s)", (name, rel))
    for pid in range(1, 6):
        for b in branches:
            qty = (pid * 37 + len(b) * 11) % 120   # varied fake stock
            cur.execute("INSERT INTO stock (product_id,branch,quantity,reorder_level) "
                        "VALUES (%s,%s,%s,50)", (pid, b, qty))
    # 3 quotations per product, varying price/delivery
    for pid in range(1, 6):
        base = 2000 + pid * 500
        for sid, (mult, days, moq) in enumerate([(1.00, 14, 100), (0.92, 25, 200), (1.05, 10, 50)], start=1):
            cur.execute("INSERT INTO quotations (supplier_id,product_id,unit_price,delivery_days,min_order_qty) "
                        "VALUES (%s,%s,%s,%s,%s)", (sid, pid, round(base * mult, 2), days, moq))
    conn.commit()
print("Seeded.")