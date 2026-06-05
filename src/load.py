import pyodbc
import pandas as pd
from src.utils import setup_logger
from config import DW_SERVER, DW_DB, DB_USER, DB_PASSWORD

logger = setup_logger(__name__)

def get_dw_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DW_SERVER};"
        f"DATABASE={DW_DB};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    return conn

IDENTITY_TABLES = ["dim_customer", "dim_product", "dim_city", "dim_salesperson"]

def load_table(df, table_name):
    logger.info(f"Loading {len(df)} rows into dw.{table_name}...")
    conn = get_dw_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM dw.{table_name}")

    cols = ", ".join(df.columns)
    placeholders = ", ".join(["?" for _ in df.columns])
    sql = f"INSERT INTO dw.{table_name} ({cols}) VALUES ({placeholders})"

    data = df.values.tolist()
    data = [
        [None if (isinstance(v, float) and pd.isna(v)) else v for v in row]
        for row in data
    ]

    if table_name in IDENTITY_TABLES:
        cursor.execute(f"SET IDENTITY_INSERT dw.{table_name} ON")

    cursor.executemany(sql, data)

    if table_name in IDENTITY_TABLES:
        cursor.execute(f"SET IDENTITY_INSERT dw.{table_name} OFF")

    conn.commit()
    conn.close()
    logger.info(f"Loaded {len(df)} rows into dw.{table_name} successfully!")

def load_customers(df):
    load_table(df, "dim_customer")

def load_products(df):
    load_table(df, "dim_product")

def load_cities(df):
    load_table(df, "dim_city")

def load_salespersons(df):
    load_table(df, "dim_salesperson")

def load_dates(df):
    load_table(df, "dim_date")

def load_sales(df):
    load_table(df, "fact_sales")