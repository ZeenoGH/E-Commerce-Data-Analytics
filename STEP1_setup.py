"""
The schema is defined here for reference assuring smooth startup,
It was created manually on Supabase By you using the SQL script version of this schema.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# -------------------------------------------------------
# Setup
# -------------------------------------------------------
load_dotenv('midterm_.env')
DATABASE_URL = os.getenv('SUPABASE_DB_URL')

Base = declarative_base()
engine = create_engine(DATABASE_URL)

print("=" * 70)
print("MIDTERM PROJECT - STEP 1: DATABASE SCHEMA (REFERENCE ONLY)")
print("=" * 70)
print("\nStudent: [Your Name]")
print("Project: E-Commerce Multi-Channel Analytics")
print("Database: PostgreSQL (Supabase)")
print("\n" + "=" * 70)

# -------------------------------------------------------
# Table 1: SUPPLIERS
# -------------------------------------------------------
class Supplier(Base):
    __tablename__ = 'suppliers'
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    country = Column(String(100))
    contact_email = Column(String(200))


# -------------------------------------------------------
# Table 2: PRODUCTS
# -------------------------------------------------------
class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    stock_quantity = Column(Integer, default=0)
    description = Column(Text)


# -------------------------------------------------------
# Table 3: CUSTOMERS
# -------------------------------------------------------
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200))
    city = Column(String(100))
    country = Column(String(100))
    signup_date = Column(DateTime, default=datetime.utcnow)


# -------------------------------------------------------
# Table 4: ORDERS
# -------------------------------------------------------
class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    channel = Column(String(50))  # 'online', 'retail', 'mobile', 'partner'
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default='pending')


# -------------------------------------------------------
# Table 5: COMPETITOR_PRICES
# -------------------------------------------------------
class CompetitorPrice(Base):
    __tablename__ = 'competitor_prices'
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    competitor = Column(String(100))
    price = Column(Float)
    date_scraped = Column(DateTime, default=datetime.utcnow)


# -------------------------------------------------------
# Info (no auto-create)
# -------------------------------------------------------
def show_schema_summary():
    print("\n[INFO] Database schema reference loaded successfully.")
    print("-" * 70)
    print("Tables defined:")
    print("  1. suppliers (PK: supplier_id)")
    print("  2. products (PK: product_id, FK: supplier_id)")
    print("  3. customers (PK: customer_id)")
    print("  4. orders (PK: order_id, FK: customer_id, product_id)")
    print("  5. competitor_prices (PK: price_id, FK: product_id)")
    print("\n[NOTE] Actual schema creation is assumed to be done manually in Supabase via SQL.")
    print("-" * 70)


if __name__ == "__main__":
    show_schema_summary()
    print("\n" + "=" * 70)
    print("[STEP 1 COMPLETE] - Schema documented, manual creation confirmed.")
    print("=" * 70)

