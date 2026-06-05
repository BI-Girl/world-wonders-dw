import pyodbc
import pandas as pd
from src.utils import setup_logger
from config import SOURCE_SERVER, SOURCE_DB, START_DATE, END_DATE, DB_USER, DB_PASSWORD

logger = setup_logger(__name__)

def get_source_connection():
    logger.info("Connecting to source database...")
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SOURCE_SERVER};"
        f"DATABASE={SOURCE_DB};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
    )
    logger.info("Connected to WideWorldImporters successfully!")
    return conn

def extract_sales():
    conn = get_source_connection()
    logger.info("Extracting sales data...")
    query = """
        SELECT
            il.InvoiceLineID,
            il.InvoiceID,
            il.StockItemID,
            il.Quantity,
            il.UnitPrice,
            il.TaxAmount,
            il.LineProfit,
            il.ExtendedPrice,
            i.InvoiceDate,
            i.CustomerID,
            i.SalespersonPersonID
        FROM Sales.InvoiceLines il
        JOIN Sales.Invoices i ON il.InvoiceID = i.InvoiceID
        WHERE i.InvoiceDate BETWEEN ? AND ?
    """
    df = pd.read_sql(query, conn, params=[START_DATE, END_DATE])
    logger.info(f"Extracted {len(df)} sales rows successfully!")
    conn.close()
    return df