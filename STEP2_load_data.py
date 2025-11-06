import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from faker import Faker
import random
from datetime import datetime, timedelta

# -------------------------------------------------------
# Setup
# -------------------------------------------------------
load_dotenv('midterm_.env')
DATABASE_URL = os.getenv('SUPABASE_DB_URL')
engine = create_engine(DATABASE_URL)
fake = Faker()

print("=" * 70)
print("MIDTERM PROJECT - STEP 2: DATA LOADING (TO EXISTING TABLES)")
print("=" * 70)

# -------------------------------------------------------
# Suppliers
# -------------------------------------------------------
def load_suppliers():
    print("[STEP 2.1] Loading Suppliers...")
    suppliers_data = [
        {'supplier_id': 1, 'name': 'TechSupply Co', 'country': 'USA', 'contact_email': 'contact@techsupply.com'},
        {'supplier_id': 2, 'name': 'Fashion Forward Ltd', 'country': 'UK', 'contact_email': 'sales@fashionforward.co.uk'},
        {'supplier_id': 3, 'name': 'Jewelry Imports Inc', 'country': 'India', 'contact_email': 'info@jewelryimports.in'},
        {'supplier_id': 4, 'name': 'Electronics Hub', 'country': 'China', 'contact_email': 'orders@electronicshub.cn'},
        {'supplier_id': 5, 'name': 'Global Retail Supply', 'country': 'Germany', 'contact_email': 'contact@globalretail.de'},
        {'supplier_id': 6, 'name': 'NordicTech AB', 'country': 'Sweden', 'contact_email': 'sales@nordictech.se'},
        {'supplier_id': 7, 'name': 'Pacific Traders', 'country': 'Australia', 'contact_email': 'info@pacifictraders.au'},
    ]
    df = pd.DataFrame(suppliers_data)
    df.to_sql('suppliers', engine, if_exists='append', index=False)
    print(f"[OK] Inserted {len(df)} suppliers into existing table.")
    return df

# -------------------------------------------------------
# Products
# -------------------------------------------------------
def load_products_from_api():
    print("\n[STEP 2.2] Loading Products from API...")
    try:
        response = requests.get('https://fakestoreapi.com/products', timeout=10)
        base_products = response.json()
        base_df = pd.DataFrame(base_products)
        base_df = base_df.rename(columns={'id': 'base_id', 'title': 'base_name'})
    except Exception as e:
        print(f"[WARN] Could not fetch from API ({e}), generating fake ones instead.")
        base_df = pd.DataFrame([{'base_id': i, 'base_name': fake.word()} for i in range(20)])
    
    categories = ['electronics', 'fashion', 'home', 'sports', 'beauty', 'toys']
    expanded = []
    for i in range(1, 501):
        base = random.choice(base_df['base_name'].tolist())
        expanded.append({
            'product_id': i,
            'name': f"{base} {random.choice(['Pro', 'Max', 'Lite', 'X', 'Mini', 'Plus'])}",
            'category': random.choice(categories),
            'price': round(random.uniform(5, 1500), 2),
            'supplier_id': random.randint(1, 7),
            'stock_quantity': random.randint(20, 1000),
            'description': fake.sentence(nb_words=12)
        })
    df = pd.DataFrame(expanded)
    df.to_sql('products', engine, if_exists='append', index=False)
    print(f"[OK] Inserted {len(df)} products into existing table.")
    return df

# -------------------------------------------------------
# Customers
# -------------------------------------------------------
def load_customers():
    print("\n[STEP 2.3] Generating Customers...")
    customers = [{
        'customer_id': i + 1,
        'name': fake.name(),
        'email': fake.email(),
        'city': fake.city(),
        'country': fake.country(),
        'signup_date': fake.date_between(start_date='-3y', end_date='today')
    } for i in range(5000)]
    df = pd.DataFrame(customers)
    df.to_sql('customers', engine, if_exists='append', index=False)
    print(f"[OK] Inserted {len(df)} customers into existing table.")
    return df


# -------------------------------------------------------
# Orders
# -------------------------------------------------------
def load_orders():
    print("\n[STEP 2.4] Generating Orders...")
    channels = ['online', 'retail', 'mobile', 'partner']
    statuses = ['completed', 'shipped', 'pending', 'returned', 'cancelled']
    orders = []

    for i in range(50000):
        product_id = random.randint(1, 500)
        customer_id = random.randint(1, 5000)
        quantity = random.randint(1, 5)
        price = random.uniform(10, 2000)
        orders.append({
            'order_id': i + 1,
            'customer_id': customer_id,
            'product_id': product_id,
            'quantity': quantity,
            'order_date': fake.date_time_between(start_date='-1y', end_date='now'),
            'channel': random.choice(channels),
            'total_amount': round(price * quantity, 2),
            'status': random.choice(statuses)
        })

    df = pd.DataFrame(orders)
    df.to_sql('orders', engine, if_exists='append', index=False)
    print(f"[OK] Inserted {len(df)} orders into existing table.")
    return df


# -------------------------------------------------------
# Competitor Prices
# -------------------------------------------------------
def load_competitor_prices():
    print("\n[STEP 2.5] Simulating Competitor Prices...")
    competitors = ['Amazon', 'eBay', 'Walmart', 'BestBuy', 'Target', 'AliExpress', 'Newegg']
    prices = []

    for product_id in range(1, 501):
        for competitor in random.sample(competitors, k=4):
            prices.append({
                'price_id': len(prices) + 1,
                'product_id': product_id,
                'competitor': competitor,
                'price': round(random.uniform(5, 1500), 2),
                'date_scraped': datetime.utcnow()
            })

    df = pd.DataFrame(prices)
    df.to_sql('competitor_prices', engine, if_exists='append', index=False)
    print(f"[OK] Inserted {len(df)} competitor prices into existing table.")
    return df


# -------------------------------------------------------
# Main
# -------------------------------------------------------
def main():
    print("\n[INFO] Assuming database schema already exists (created via SQL script).")
    print("[INFO] Starting data loading process...\n")

    load_suppliers()
    load_products_from_api()
    load_customers()
    load_orders()
    load_competitor_prices()

    print("\n" + "=" * 70)
    print("[SUCCESS] ALL DATA LOADED INTO EXISTING TABLES!")
    print("=" * 70)


if __name__ == "__main__":
    main()