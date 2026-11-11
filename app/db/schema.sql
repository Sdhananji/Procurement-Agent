CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT
);

CREATE TABLE stock (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    branch TEXT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 0
);

CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    reliability_score NUMERIC(3,2) DEFAULT 0.80   -- 0 to 1
);

CREATE TABLE quotations (
    id SERIAL PRIMARY KEY,
    supplier_id INT REFERENCES suppliers(id),
    product_id INT REFERENCES products(id),
    unit_price NUMERIC(10,2) NOT NULL,
    delivery_days INT NOT NULL,
    min_order_qty INT DEFAULT 1,
    valid_until DATE,
    source_file TEXT
);

CREATE TABLE purchase_requests (
    id SERIAL PRIMARY KEY,
    requested_by TEXT,
    branch TEXT,
    request_text TEXT NOT NULL,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE purchase_orders (
    id SERIAL PRIMARY KEY,
    request_id INT REFERENCES purchase_requests(id),
    supplier_id INT REFERENCES suppliers(id),
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10,2),
    total_amount NUMERIC(12,2),
    status TEXT DEFAULT 'pending_approval',
    approved_by TEXT,
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    entity TEXT,
    entity_id INT,
    action TEXT,
    actor TEXT,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);