#  MIDTERM PROJECT - VALIDATION & CRUD OPERATIONS GUIDE

## Student: Zinaddine Ghanemi
## Course: MADSC102 - Unlocking the Power of Big Data
## Date: November 6, 2025

---

##  DATABASE SCHEMA OVERVIEW

```
SUPPLIERS (7 records)
├─ PK: supplier_id
├─ name, country, contact_email
└─ Relationships: One-to-Many with PRODUCTS

PRODUCTS (500 records)
├─ PK: product_id
├─ FK: supplier_id → SUPPLIERS
├─ name, category, price, stock_quantity, description
└─ Relationships: One-to-Many with ORDERS

CUSTOMERS (5,000 records)
├─ PK: customer_id
├─ name, email (unique), city, country, signup_date
└─ Relationships: One-to-Many with ORDERS

ORDERS (50,000 records)
├─ PK: order_id
├─ FK: customer_id → CUSTOMERS
├─ FK: product_id → PRODUCTS
└─ quantity, order_date, channel, total_amount, status

COMPETITOR_PRICES (2,000+ records)
├─ PK: price_id
├─ FK: product_id → PRODUCTS
└─ competitor, price, date_scraped
```

---

## 🔧 INDIVIDUAL CRUD OPERATIONS FOR SUPABASE

### How to Run These in Supabase:
1. Go to your Supabase project
2. Click on "SQL Editor" in the left sidebar
3. Copy and paste each SQL block below
4. Click "Run" or press Ctrl+Enter
5. View results in the output panel

---

##  CREATE OPERATIONS

### Operation 1A: Insert a New Customer

```sql
-- INSERT NEW CUSTOMER
INSERT INTO customers (name, email, city, country, signup_date)
VALUES 
    ('Zinaddine Ghanemi', 'zinaddine.ghanemi@student.com', 'Leipzig', 'Germany', CURRENT_DATE)
RETURNING *;
```

**Expected Output:** New customer record with auto-generated customer_id

**Business Use Case:** Register new customer in the system

---

### Operation 1B: Insert a New Order

```sql
-- INSERT NEW ORDER
-- First, let's get a valid customer_id and product_id
INSERT INTO orders (customer_id, product_id, quantity, order_date, channel, total_amount, status)
VALUES 
    (1, 10, 2, CURRENT_TIMESTAMP, 'online', 299.98, 'pending')
RETURNING *;
```

**Expected Output:** New order record with auto-generated order_id

**Business Use Case:** Record a new customer purchase

---

### Operation 1C: Insert Multiple Products

```sql
-- INSERT MULTIPLE NEW PRODUCTS AT ONCE
INSERT INTO products (name, category, price, supplier_id, stock_quantity, description)
VALUES 
    ('Smart Watch Pro', 'electronics', 249.99, 1, 150, 'Advanced fitness tracker with heart rate monitor'),
    ('Wireless Earbuds Max', 'electronics', 179.99, 1, 200, 'Premium noise-cancelling earbuds'),
    ('Gaming Mouse RGB', 'electronics', 89.99, 4, 300, 'High-precision gaming mouse with RGB lighting')
RETURNING product_id, name, price;
```

**Expected Output:** 3 new products with their IDs

**Business Use Case:** Bulk add new products to inventory

---

## 2️⃣ READ OPERATIONS

### Operation 2A: Simple Select with Filter

```sql
-- READ: Get all orders above $500
SELECT 
    order_id,
    customer_id,
    product_id,
    quantity,
    total_amount,
    order_date,
    channel,
    status
FROM orders
WHERE total_amount > 500
ORDER BY total_amount DESC
LIMIT 20;
```

**Expected Output:** List of high-value orders

**Business Use Case:** Identify premium transactions for VIP customer analysis

---

### Operation 2B: Read with JOIN (2 tables)

```sql
-- READ: Customer orders with product details
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.email,
    c.city,
    o.order_id,
    o.order_date,
    o.total_amount,
    o.channel,
    o.status
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 100
ORDER BY o.order_date DESC
LIMIT 25;
```

**Expected Output:** Orders linked to customer information

**Business Use Case:** Customer purchase history analysis

---

### Operation 2C: Read with Complex JOIN (3 tables)

```sql
-- READ: Complete order details with customer and product info
SELECT 
    o.order_id,
    o.order_date,
    o.channel,
    o.status,
    c.name AS customer_name,
    c.email AS customer_email,
    c.city,
    c.country,
    p.name AS product_name,
    p.category,
    p.price AS unit_price,
    o.quantity,
    o.total_amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON o.product_id = p.product_id
WHERE o.channel = 'online' 
    AND o.total_amount > 200
ORDER BY o.order_date DESC
LIMIT 30;
```

**Expected Output:** Complete transaction details with all related information

**Business Use Case:** Full transaction audit trail for online high-value orders

---

### Operation 2D: Read with Aggregation (GROUP BY)

```sql
-- READ: Revenue by Channel
SELECT 
    channel,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    MIN(total_amount) AS min_order,
    MAX(total_amount) AS max_order
FROM orders
GROUP BY channel
ORDER BY total_revenue DESC;
```

**Expected Output:** Revenue metrics broken down by sales channel

**Business Use Case:** Channel performance comparison for strategic planning

---

### Operation 2E: Read Top Customers

```sql
-- READ: Top 10 Customers by Lifetime Value
SELECT 
    c.customer_id,
    c.name,
    c.email,
    c.city,
    c.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.city, c.country
HAVING COUNT(o.order_id) > 0
ORDER BY lifetime_value DESC
LIMIT 10;
```

**Expected Output:** Top 10 most valuable customers

**Business Use Case:** VIP customer identification for loyalty programs

---

### Operation 2F: Read Product Performance

```sql
-- READ: Best Selling Products
SELECT 
    p.product_id,
    p.name AS product_name,
    p.category,
    p.price,
    COUNT(o.order_id) AS times_ordered,
    SUM(o.quantity) AS total_units_sold,
    SUM(o.total_amount) AS total_revenue
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.name, p.category, p.price
HAVING COUNT(o.order_id) > 0
ORDER BY total_revenue DESC
LIMIT 15;
```

**Expected Output:** Top performing products by revenue

**Business Use Case:** Inventory optimization and marketing focus

---

## 3️ UPDATE OPERATIONS

### Operation 3A: Update Order Status (Single Record)

```sql
-- UPDATE: Change order status from pending to shipped
UPDATE orders
SET status = 'shipped'
WHERE order_id = 1
RETURNING order_id, status, order_date, total_amount;
```

**Expected Output:** Updated order showing new status

**Business Use Case:** Order fulfillment workflow

---

### Operation 3B: Update Multiple Records with Condition

```sql
-- UPDATE: Mark all old pending orders as shipped
UPDATE orders
SET status = 'shipped'
WHERE status = 'pending' 
    AND order_date < CURRENT_DATE - INTERVAL '7 days'
RETURNING order_id, status, order_date;
```

**Expected Output:** All updated orders with new status

**Business Use Case:** Automated order status updates for logistics

---

### Operation 3C: Update Product Prices (Bulk Update)

```sql
-- UPDATE: Increase electronics prices by 10%
UPDATE products
SET price = ROUND((price * 1.10)::numeric, 2)
WHERE category = 'electronics'
RETURNING product_id, name, category, price;
```

**Expected Output:** Updated products with new prices

**Business Use Case:** Dynamic pricing adjustments

---

### Operation 3D: Update Customer Information

```sql
-- UPDATE: Update customer email and city
UPDATE customers
SET 
    email = 'new.email@example.com',
    city = 'Berlin'
WHERE customer_id = 1
RETURNING customer_id, name, email, city, country;
```

**Expected Output:** Updated customer record

**Business Use Case:** Customer profile maintenance

---

### Operation 3E: Update Stock Quantity After Sales

```sql
-- UPDATE: Reduce stock after order
UPDATE products
SET stock_quantity = stock_quantity - 5
WHERE product_id = 10
    AND stock_quantity >= 5
RETURNING product_id, name, stock_quantity;
```

**Expected Output:** Updated product with new stock level

**Business Use Case:** Inventory management after sales

---

## 4️⃣ DELETE OPERATIONS

### Operation 4A: Safe Delete with WHERE (Single Record)

```sql
-- DELETE: Remove a specific cancelled order
DELETE FROM orders
WHERE order_id = 100
    AND status = 'cancelled'
RETURNING order_id, status, order_date, total_amount;
```

**Expected Output:** Deleted order details (if found)

**Business Use Case:** Clean up cancelled transactions

---

### Operation 4B: Delete Old Records (Data Retention)

```sql
-- DELETE: Remove old competitor prices (older than 60 days)
DELETE FROM competitor_prices
WHERE date_scraped < CURRENT_DATE - INTERVAL '60 days'
RETURNING price_id, product_id, competitor, date_scraped;
```

**Expected Output:** List of deleted old price records

**Business Use Case:** Data retention policy enforcement

---

### Operation 4C: Delete with Multiple Conditions

```sql
-- DELETE: Remove cancelled orders older than 30 days
DELETE FROM orders
WHERE status = 'cancelled'
    AND order_date < CURRENT_DATE - INTERVAL '30 days'
RETURNING order_id, customer_id, order_date, status;
```

**Expected Output:** Deleted cancelled orders

**Business Use Case:** Archive management and database cleanup

---

### Operation 4D: Safe Delete with Subquery

```sql
-- DELETE: Remove products with no orders and low stock
DELETE FROM products
WHERE product_id NOT IN (SELECT DISTINCT product_id FROM orders)
    AND stock_quantity < 10
RETURNING product_id, name, category, stock_quantity;
```

**Expected Output:** Deleted obsolete products

**Business Use Case:** Inventory cleanup for discontinued items

---

## 📋 VERIFICATION QUERIES

### Verify Data After CRUD Operations:

```sql
-- Count records in each table
SELECT 
    'suppliers' AS table_name, COUNT(*) AS record_count FROM suppliers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'competitor_prices', COUNT(*) FROM competitor_prices
ORDER BY table_name;
```

---

### Check Foreign Key Relationships:

```sql
-- Verify referential integrity
SELECT 
    'Orders with invalid customer_id' AS check_name,
    COUNT(*) AS violations
FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM customers c WHERE c.customer_id = o.customer_id)

UNION ALL

SELECT 
    'Orders with invalid product_id',
    COUNT(*)
FROM orders o
WHERE NOT EXISTS (SELECT 1 FROM products p WHERE p.product_id = o.product_id)

UNION ALL

SELECT 
    'Products with invalid supplier_id',
    COUNT(*)
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM suppliers s WHERE s.supplier_id = p.supplier_id);
```

Expected: All counts should be 0 (no violations)

---

## VIEWS (Required: 1, Delivered: 3)

### View 1: Complete Order Details

```sql
-- CREATE VIEW: Order details with customer and product info
CREATE OR REPLACE VIEW vw_order_details AS
SELECT 
    o.order_id,
    o.order_date,
    o.channel,
    o.status,
    c.customer_id,
    c.name AS customer_name,
    c.email AS customer_email,
    c.city AS customer_city,
    c.country AS customer_country,
    p.product_id,
    p.name AS product_name,
    p.category AS product_category,
    p.price AS unit_price,
    o.quantity,
    o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id;

-- Query the view
SELECT * FROM vw_order_details
WHERE channel = 'online'
ORDER BY order_date DESC
LIMIT 20;
```

---

### View 2: Product Revenue Analysis

```sql
-- CREATE VIEW: Product performance metrics
CREATE OR REPLACE VIEW vw_product_revenue AS
SELECT 
    p.product_id,
    p.name AS product_name,
    p.category,
    p.price AS current_price,
    s.name AS supplier_name,
    s.country AS supplier_country,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.quantity), 0) AS units_sold,
    COALESCE(SUM(o.total_amount), 0) AS total_revenue,
    COALESCE(AVG(o.total_amount), 0) AS avg_order_value,
    p.stock_quantity
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
GROUP BY p.product_id, p.name, p.category, p.price, s.name, s.country, p.stock_quantity;

-- Query the view
SELECT * FROM vw_product_revenue
WHERE total_revenue > 0
ORDER BY total_revenue DESC
LIMIT 15;
```

---

### View 3: Customer Lifetime Value

```sql
-- CREATE VIEW: Customer summary with lifetime value
CREATE OR REPLACE VIEW vw_customer_summary AS
SELECT 
    c.customer_id,
    c.name AS customer_name,
    c.email,
    c.city,
    c.country,
    c.signup_date,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS lifetime_value,
    COALESCE(AVG(o.total_amount), 0) AS avg_order_value,
    MAX(o.order_date) AS last_order_date,
    CASE 
        WHEN COALESCE(SUM(o.total_amount), 0) > 1000 THEN 'VIP'
        WHEN COALESCE(SUM(o.total_amount), 0) > 500 THEN 'High Value'
        WHEN COALESCE(SUM(o.total_amount), 0) > 200 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.email, c.city, c.country, c.signup_date;

-- Query the view
SELECT * FROM vw_customer_summary
WHERE lifetime_value > 0
ORDER BY lifetime_value DESC
LIMIT 20;
```

---

##  ANALYTICAL QUERIES (Business Questions)

### Query 1: Answer Main Business Question

```sql
-- "Which products generate the most revenue across different sales channels?"
SELECT 
    p.name AS product_name,
    p.category,
    o.channel,
    COUNT(o.order_id) AS orders_count,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM products p
JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.name, p.category, o.channel
HAVING SUM(o.total_amount) > 1000
ORDER BY total_revenue DESC
LIMIT 20;
```

**Business Insight:** Identifies top-performing products by channel for inventory optimization

---

### Query 2: Channel Performance Comparison

```sql
-- Revenue and order metrics by channel
SELECT 
    channel,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue,
    AVG(total_amount) AS avg_order_value,
    MIN(total_amount) AS min_order,
    MAX(total_amount) AS max_order,
    ROUND(SUM(total_amount) * 100.0 / SUM(SUM(total_amount)) OVER (), 2) AS revenue_percentage
FROM orders
WHERE status NOT IN ('cancelled', 'returned')
GROUP BY channel
ORDER BY total_revenue DESC;
```

**Business Insight:** Shows which channel drives the most revenue and customer engagement

---

### Query 3: Category Performance

```sql
-- Revenue by product category
SELECT 
    category,
    COUNT(DISTINCT p.product_id) AS products_count,
    COUNT(o.order_id) AS orders_count,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS total_revenue,
    AVG(p.price) AS avg_product_price,
    AVG(o.total_amount) AS avg_order_value
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY category
ORDER BY total_revenue DESC;
```

**Business Insight:** Identifies most profitable product categories

---

### Query 4: Time-Based Analysis

```sql
-- Monthly revenue trend
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    channel,
    COUNT(order_id) AS orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS avg_order_value
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY DATE_TRUNC('month', order_date), channel
ORDER BY month DESC, revenue DESC;
```

**Business Insight:** Shows seasonal trends and channel performance over time

---

**Database:** PostgreSQL (Supabase)

**Status:** ✅ READY FOR SUBMISSION
