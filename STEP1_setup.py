"""
MIDTERM PROJECT - STEP 1: Database Setup
Creates the complete schema with 5 tables and relationships
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Load environment
load_dotenv('midterm_.env')
DATABASE_URL = os.getenv('SUPABASE_DB_URL')

Base = declarative_base()
engine = create_engine(DATABASE_URL)

print("="*70)
print("MIDTERM PROJECT - DATABASE SETUP")
print("="*70)
print("\nStudent: [Your Name]")
print("Project: E-Commerce Multi-Channel Analytics")
print("Database: PostgreSQL (Supabase)")
print("\n" + "="*70)

# Table 1: SUPPLIERS
class Supplier(Base):
    __tablename__ = 'suppliers'
    
    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    country = Column(String(100))
    contact_email = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)

# Table 2: PRODUCTS
class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    stock_quantity = Column(Integer, default=0)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Table 3: CUSTOMERS
class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    signup_date = Column(DateTime, default=datetime.utcnow)

# Table 4: ORDERS
class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    channel = Column(String(50))  # 'online', 'retail', 'mobile'
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default='pending')

# Table 5: COMPETITOR_PRICES
class CompetitorPrice(Base):
    __tablename__ = 'competitor_prices'
    
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(500))
    competitor = Column(String(100))
    price = Column(Float)
    date_scraped = Column(DateTime, default=datetime.utcnow)

def create_schema():
    """Create all tables"""
    print("\n[STEP 1] Creating database schema...")
    print("-" * 70)
    
    try:
        # Drop existing tables (for clean slate)
        print("\nDropping existing tables (if any)...")
        Base.metadata.drop_all(engine)
        print("[OK] Old tables dropped")
        
        # Create new tables
        print("\nCreating new tables...")
        Base.metadata.create_all(engine)
        
        print("\n[SUCCESS] All tables created!")
        print("\nTables created:")
        print("  1. suppliers (PK: supplier_id)")
        print("  2. products (PK: product_id, FK: supplier_id)")
        print("  3. customers (PK: customer_id)")
        print("  4. orders (PK: order_id, FK: customer_id, product_id)")
        print("  5. competitor_prices (PK: price_id)")
        
        print("\n[OK] Database schema is ready!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Failed to create schema: {e}")
        return False

if __name__ == "__main__":
    success = create_schema()
    
    if success:
        print("\n" + "="*70)
        print("[SUCCESS] STEP 1 COMPLETE - Database Ready!")
        print("="*70)
        print("\nNext: Run STEP 2 to load data")
    else:
        print("\n" + "="*70)
        print("[ERROR] Setup failed - Check your database credentials")
        print("="*70)
