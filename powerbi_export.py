import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# -------------------------------------------------------
# Setup
# -------------------------------------------------------
load_dotenv('midterm_.env')
DATABASE_URL = os.getenv('SUPABASE_DB_URL')
engine = create_engine(DATABASE_URL)

print("=" * 70)
print("MIDTERM PROJECT - STEP 6: POWER BI DATA EXPORT")
print("=" * 70)


# -------------------------------------------------------
# Export Tables
# -------------------------------------------------------
def export_tables():
    """Export core tables from the existing database schema"""
    print("\n[STEP 6.1] Exporting Core Tables...")
    print("-" * 70)

    tables = ['suppliers', 'products', 'customers', 'orders', 'competitor_prices']

    for table in tables:
        try:
            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, engine)
            filename = f"powerbi_{table}.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"[OK] Exported {table}: {len(df)} records → {filename}")
        except Exception as e:
            print(f"[WARN] Could not export {table}: {e}")

    print("\n[INFO] All available tables exported successfully.")
    print("-" * 70)


# -------------------------------------------------------
# Main
# -------------------------------------------------------
def main():
    print("[INFO] Assuming database schema already exists and data is loaded (Steps 1–5).")
    print("[INFO] Starting Power BI export process...")
    export_tables()

    print("\n" + "=" * 70)
    print("[SUCCESS] POWER BI EXPORT COMPLETE!")
    print("=" * 70)
    print("\nCSV files generated:")
    print("  - powerbi_suppliers.csv")
    print("  - powerbi_products.csv")
    print("  - powerbi_customers.csv")
    print("  - powerbi_orders.csv")
    print("  - powerbi_competitor_prices.csv")
    print("\nThese files are ready for import into Power BI Desktop.")


if __name__ == "__main__":
    main()
