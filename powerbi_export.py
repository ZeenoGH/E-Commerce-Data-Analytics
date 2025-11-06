"""
MIDTERM PROJECT - STEP 6: POWER BI EXPORT
Exports all data in Power BI-friendly format
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv('midterm_.env')
DATABASE_URL = os.getenv('SUPABASE_DB_URL')
engine = create_engine(DATABASE_URL)

print("="*70)
print("MIDTERM PROJECT - POWER BI DATA EXPORT")
print("="*70)

def export_tables():
    """Export all tables for Power BI"""
    print("\n[STEP 6.1] Exporting Tables...")
    print("-" * 70)
    
    tables = ['suppliers', 'products', 'customers', 'orders', 'competitor_prices']
    
    for table in tables:
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(query, engine)
        filename = f'powerbi_{table}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"[OK] Exported {table}: {len(df)} records → {filename}")

def export_views():
    """Export JOIN views for Power BI"""
    print("\n[STEP 6.2] Exporting Views...")
    print("-" * 70)
    
    views = {
        'vw_order_details': 'powerbi_order_details.csv',
        'vw_product_revenue': 'powerbi_product_revenue.csv',
        'vw_customer_summary': 'powerbi_customer_summary.csv'
    }
    
    for view, filename in views.items():
        query = f"SELECT * FROM {view}"
        df = pd.read_sql(query, engine)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"[OK] Exported {view}: {len(df)} records → {filename}")

def create_analytics_tables():
    """Create aggregated tables for Power BI dashboards"""
    print("\n[STEP 6.3] Creating Analytics Tables...")
    print("-" * 70)
    
    # 1. Revenue by Channel & Month
    query1 = """
    SELECT 
        EXTRACT(YEAR FROM order_date) as year,
        EXTRACT(MONTH FROM order_date) as month,
        channel,
        COUNT(*) as order_count,
        SUM(total_amount) as revenue,
        AVG(total_amount) as avg_order_value
    FROM orders
    GROUP BY year, month, channel
    ORDER BY year, month, channel;
    """
    df1 = pd.read_sql(query1, engine)
    df1.to_csv('powerbi_revenue_by_channel_month.csv', index=False, encoding='utf-8-sig')
    print(f"[OK] Revenue by Channel/Month: {len(df1)} records")
    
    # 2. Product Performance
    query2 = """
    SELECT 
        p.product_id,
        p.name as product_name,
        p.category,
        p.price,
        COUNT(o.order_id) as times_ordered,
        SUM(o.quantity) as units_sold,
        SUM(o.total_amount) as total_revenue,
        p.stock_quantity
    FROM products p
    LEFT JOIN orders o ON p.product_id = o.product_id
    GROUP BY p.product_id, p.name, p.category, p.price, p.stock_quantity;
    """
    df2 = pd.read_sql(query2, engine)
    df2.to_csv('powerbi_product_performance.csv', index=False, encoding='utf-8-sig')
    print(f"[OK] Product Performance: {len(df2)} records")
    
    # 3. Customer Segments
    query3 = """
    SELECT 
        c.customer_id,
        c.name,
        c.country,
        c.city,
        COUNT(o.order_id) as total_orders,
        SUM(o.total_amount) as lifetime_value,
        AVG(o.total_amount) as avg_order_value,
        CASE 
            WHEN SUM(o.total_amount) > 1000 THEN 'VIP'
            WHEN SUM(o.total_amount) > 500 THEN 'High Value'
            WHEN SUM(o.total_amount) > 200 THEN 'Medium Value'
            ELSE 'Low Value'
        END as segment
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name, c.country, c.city;
    """
    df3 = pd.read_sql(query3, engine)
    df3.to_csv('powerbi_customer_segments.csv', index=False, encoding='utf-8-sig')
    print(f"[OK] Customer Segments: {len(df3)} records")
    
    # 4. Competitor Price Comparison
    query4 = """
    SELECT 
        product_name,
        competitor,
        price,
        date_scraped
    FROM competitor_prices
    ORDER BY product_name, competitor;
    """
    df4 = pd.read_sql(query4, engine)
    df4.to_csv('powerbi_competitor_analysis.csv', index=False, encoding='utf-8-sig')
    print(f"[OK] Competitor Analysis: {len(df4)} records")

def create_ml_export():
    """Export ML predictions for Power BI"""
    print("\n[STEP 6.4] Exporting ML Predictions...")
    print("-" * 70)
    
    try:
        query = "SELECT * FROM ml_predictions LIMIT 100"
        df = pd.read_sql(query, engine)
        df.to_csv('powerbi_ml_predictions.csv', index=False, encoding='utf-8-sig')
        print(f"[OK] ML Predictions: {len(df)} records")
    except:
        print("[INFO] No ML predictions table found (run STEP 5 first)")

def create_powerbi_guide():
    """Create Power BI import guide"""
    print("\n[STEP 6.5] Creating Power BI Guide...")
    print("-" * 70)
    
    guide = """
================================================================================
POWER BI IMPORT & DASHBOARD GUIDE
================================================================================

FILES TO IMPORT (11 CSV Files):
-------------------------------
Core Tables:
1. powerbi_suppliers.csv
2. powerbi_products.csv
3. powerbi_customers.csv
4. powerbi_orders.csv
5. powerbi_competitor_prices.csv

Views:
6. powerbi_order_details.csv
7. powerbi_product_revenue.csv
8. powerbi_customer_summary.csv

Analytics:
9. powerbi_revenue_by_channel_month.csv
10. powerbi_product_performance.csv
11. powerbi_customer_segments.csv
12. powerbi_competitor_analysis.csv
13. powerbi_ml_predictions.csv (if available)

================================================================================
SUGGESTED POWER BI DASHBOARDS
================================================================================

DASHBOARD 1: EXECUTIVE OVERVIEW
-------------------------------
Visuals:
- Card: Total Revenue
- Card: Total Orders
- Card: Total Customers
- Card: Average Order Value
- Line Chart: Revenue Trend by Month
- Pie Chart: Revenue by Channel
- Bar Chart: Top 10 Products
- Map: Sales by Country

Data Source: powerbi_order_details.csv, powerbi_product_revenue.csv

DASHBOARD 2: SALES ANALYSIS
----------------------------
Visuals:
- Matrix: Revenue by Category & Channel
- Column Chart: Monthly Revenue by Channel
- Line Chart: Order Volume Trend
- Scatter Plot: Price vs Revenue
- Table: Top 10 Best Selling Products

Data Source: powerbi_revenue_by_channel_month.csv, powerbi_product_performance.csv

DASHBOARD 3: CUSTOMER INSIGHTS
-------------------------------
Visuals:
- Donut Chart: Customer Segments
- Bar Chart: Top 10 Customers by Lifetime Value
- Table: VIP Customers Details
- Map: Customer Distribution by Country
- Gauge: Customer Retention Rate

Data Source: powerbi_customer_segments.csv, powerbi_customer_summary.csv

DASHBOARD 4: PRODUCT PERFORMANCE
---------------------------------
Visuals:
- Bar Chart: Revenue by Category
- Table: Product Performance Metrics
- Scatter: Price vs Units Sold
- KPI: Low Stock Alert (stock < 20)
- Tree Map: Revenue by Product

Data Source: powerbi_product_performance.csv

DASHBOARD 5: COMPETITOR ANALYSIS
---------------------------------
Visuals:
- Table: Price Comparison (Our Price vs Competitors)
- Bar Chart: Average Competitor Price by Product
- Scatter: Our Price Position vs Market
- Card: % Products Competitively Priced

Data Source: powerbi_competitor_analysis.csv, powerbi_products.csv

DASHBOARD 6: ML INSIGHTS (OPTIONAL)
------------------------------------
Visuals:
- Scatter: Predicted vs Actual Revenue
- Card: Model Accuracy
- Line Chart: Prediction Trend
- Table: Top Prediction Errors

Data Source: powerbi_ml_predictions.csv

================================================================================
DATA RELATIONSHIPS
================================================================================

Set up these relationships in Power BI:

products.product_id → orders.product_id (Many-to-One)
customers.customer_id → orders.customer_id (Many-to-One)
suppliers.supplier_id → products.supplier_id (Many-to-One)

================================================================================
MEASURES TO CREATE (DAX)
================================================================================

1. Total Revenue = SUM(orders[total_amount])

2. Average Order Value = AVERAGE(orders[total_amount])

3. Total Orders = COUNTROWS(orders)

4. Revenue Growth % = 
   DIVIDE(
       [Total Revenue] - CALCULATE([Total Revenue], DATEADD(orders[order_date], -1, MONTH)),
       CALCULATE([Total Revenue], DATEADD(orders[order_date], -1, MONTH))
   )

5. Customer Lifetime Value = 
   SUMX(
       VALUES(customers[customer_id]),
       CALCULATE(SUM(orders[total_amount]))
   )

6. Top 10 Products = 
   TOPN(10, VALUES(products[name]), [Total Revenue], DESC)

================================================================================
FILTERS & SLICERS
================================================================================

Add these slicers to your dashboards:
- Date Range (order_date)
- Channel (online/retail/mobile)
- Category (product category)
- Country (customer country)
- Customer Segment (VIP/High/Medium/Low)

================================================================================
COLOR SCHEME SUGGESTIONS
================================================================================

- Primary: #2E86AB (Blue)
- Secondary: #E63946 (Red)
- Accent 1: #F77F00 (Orange)
- Accent 2: #06FFA5 (Green)
- Neutral: #F1F1F1 (Light Gray)

================================================================================
TIPS FOR BEST PRACTICE
================================================================================

1. Use consistent formatting across all dashboards
2. Add tooltips for better user experience
3. Enable drill-through for detailed analysis
4. Use bookmarks for different views
5. Add navigation buttons between dashboards
6. Set up row-level security if needed
7. Publish to Power BI Service for sharing

================================================================================
NEXT STEPS
================================================================================

1. Import all CSV files to Power BI Desktop
2. Set up relationships in Model view
3. Create calculated measures
4. Build dashboards following the structure above
5. Apply filters and format visuals
6. Test all interactions
7. Publish to Power BI Service

================================================================================
"""
    
    with open('POWERBI_COMPLETE_GUIDE.txt', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("[OK] Guide created: POWERBI_COMPLETE_GUIDE.txt")

def main():
    export_tables()
    export_views()
    create_analytics_tables()
    create_ml_export()
    create_powerbi_guide()
    
    print("\n" + "="*70)
    print("[SUCCESS] POWER BI EXPORT COMPLETE!")
    print("="*70)
    print("\nFiles created (13 CSV files):")
    print("  Core Tables: 5 files")
    print("  Views: 3 files")
    print("  Analytics: 4 files")
    print("  ML: 1 file")
    print("  Guide: POWERBI_COMPLETE_GUIDE.txt")
    print("\nAll files are UTF-8 encoded and ready for Power BI import!")
    print("\nNext Steps:")
    print("  1. Open Power BI Desktop")
    print("  2. Import all CSV files")
    print("  3. Follow POWERBI_COMPLETE_GUIDE.txt")
    print("  4. Create 6 suggested dashboards")

if __name__ == "__main__":
    main()
