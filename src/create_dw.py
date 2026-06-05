import pyodbc
from src.utils import setup_logger
from config import DW_SERVER, DW_DB, DB_USER, DB_PASSWORD

logger = setup_logger(__name__)

def get_dw_connection(database="master"):
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DW_SERVER};"
        f"DATABASE={database};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    conn.autocommit = True
    return conn

def create_database():
    logger.info("Creating WorldWondersDW database...")
    conn = get_dw_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'WorldWondersDW')
        CREATE DATABASE WorldWondersDW
    """)
    logger.info("WorldWondersDW database ready!")
    conn.close()

def create_schema():
    logger.info("Creating dw schema...")
    conn = get_dw_connection(DW_DB)
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'dw')
        EXEC('CREATE SCHEMA dw')
    """)
    logger.info("Schema dw ready!")
    conn.close()

def create_dimensions():
    logger.info("Creating dimension tables...")
    conn = get_dw_connection(DW_DB)
    cursor = conn.cursor()

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dim_customer')
        CREATE TABLE dw.dim_customer (
            customer_key INT IDENTITY(1,1) PRIMARY KEY,
            customer_id INT,
            customer_name NVARCHAR(100),
            category NVARCHAR(50),
            buying_group NVARCHAR(50),
            credit_limit DECIMAL(18,2)
        )
    """)

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dim_product')
        CREATE TABLE dw.dim_product (
            product_key INT IDENTITY(1,1) PRIMARY KEY,
            stock_item_id INT,
            product_name NVARCHAR(200),
            color NVARCHAR(50),
            unit_price DECIMAL(18,2),
            stock_group NVARCHAR(50)
        )
    """)

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dim_city')
        CREATE TABLE dw.dim_city (
            city_key INT IDENTITY(1,1) PRIMARY KEY,
            city_id INT,
            city_name NVARCHAR(50),
            state_province NVARCHAR(50),
            country NVARCHAR(50),
            sales_territory NVARCHAR(50)
        )
    """)

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dim_salesperson')
        CREATE TABLE dw.dim_salesperson (
            salesperson_key INT IDENTITY(1,1) PRIMARY KEY,
            person_id INT,
            full_name NVARCHAR(50),
            preferred_name NVARCHAR(50),
            email NVARCHAR(256)
        )
    """)

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='dim_date')
        CREATE TABLE dw.dim_date (
            date_key INT PRIMARY KEY,
            full_date DATE,
            day_of_week INT,
            day_name NVARCHAR(10),
            month INT,
            month_name NVARCHAR(10),
            quarter INT,
            year INT,
            is_weekend BIT
        )
    """)

    logger.info("All dimension tables created!")
    conn.close()

def create_facts():
    logger.info("Creating fact table...")
    conn = get_dw_connection(DW_DB)
    cursor = conn.cursor()

    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='fact_sales')
        CREATE TABLE dw.fact_sales (
            sales_key INT IDENTITY(1,1) PRIMARY KEY,
            invoice_line_id INT,
            invoice_id INT,
            customer_key INT FOREIGN KEY REFERENCES dw.dim_customer(customer_key),
            product_key INT FOREIGN KEY REFERENCES dw.dim_product(product_key),
            salesperson_key INT FOREIGN KEY REFERENCES dw.dim_salesperson(salesperson_key),
            date_key INT FOREIGN KEY REFERENCES dw.dim_date(date_key),
            quantity INT,
            unit_price DECIMAL(18,2),
            tax_amount DECIMAL(18,2),
            line_profit DECIMAL(18,2),
            extended_price DECIMAL(18,2)
        )
    """)

    logger.info("fact_sales table created!")
    conn.close()

def run_create_dw():
    logger.info("===== Starting DW creation =====")
    create_database()
    create_schema()
    create_dimensions()
    create_facts()
    logger.info("===== DW creation complete! =====")