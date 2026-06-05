import pyodbc
import pandas as pd
from src.utils import setup_logger
from config import SOURCE_SERVER, SOURCE_DB, DB_USER, DB_PASSWORD, START_DATE, END_DATE

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
    logger.info("Connected to WideWorldImporters!")
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
    logger.info(f"Extracted {len(df)} sales rows!")
    conn.close()
    return df

def extract_customers():
    conn = get_source_connection()
    logger.info("Extracting customers...")
    query = """
        SELECT
            c.CustomerID,
            c.CustomerName,
            cc.CustomerCategoryName,
            bg.BuyingGroupName,
            c.CreditLimit
        FROM Sales.Customers c
        LEFT JOIN Sales.CustomerCategories cc
            ON c.CustomerCategoryID = cc.CustomerCategoryID
        LEFT JOIN Sales.BuyingGroups bg
            ON c.BuyingGroupID = bg.BuyingGroupID
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} customers!")
    conn.close()
    return df

def extract_products():
    conn = get_source_connection()
    logger.info("Extracting products...")
    query = """
        SELECT
            si.StockItemID,
            si.StockItemName,
            c.ColorName,
            si.UnitPrice,
            sg.StockGroupName
        FROM Warehouse.StockItems si
        LEFT JOIN Warehouse.Colors c
            ON si.ColorID = c.ColorID
        LEFT JOIN Warehouse.StockItemStockGroups sisg
            ON si.StockItemID = sisg.StockItemID
        LEFT JOIN Warehouse.StockGroups sg
            ON sisg.StockGroupID = sg.StockGroupID
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} products!")
    conn.close()
    return df

def extract_cities():
    conn = get_source_connection()
    logger.info("Extracting cities...")
    query = """
        SELECT
            ci.CityID,
            ci.CityName,
            sp.StateProvinceName,
            co.CountryName,
            sp.SalesTerritory
        FROM Application.Cities ci
        LEFT JOIN Application.StateProvinces sp
            ON ci.StateProvinceID = sp.StateProvinceID
        LEFT JOIN Application.Countries co
            ON sp.CountryID = co.CountryID
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} cities!")
    conn.close()
    return df

def extract_salespersons():
    conn = get_source_connection()
    logger.info("Extracting salespersons...")
    query = """
        SELECT
            PersonID,
            FullName,
            PreferredName,
            EmailAddress
        FROM Application.People
        WHERE IsSalesperson = 1
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} salespersons!")
    conn.close()
    return df

def extract_customers():
    conn = get_source_connection()
    logger.info("Extracting customers...")
    query = """
        SELECT
            c.CustomerID,
            c.CustomerName,
            cc.CustomerCategoryName,
            bg.BuyingGroupName,
            c.CreditLimit
        FROM Sales.Customers c
        LEFT JOIN Sales.CustomerCategories cc
            ON c.CustomerCategoryID = cc.CustomerCategoryID
        LEFT JOIN Sales.BuyingGroups bg
            ON c.BuyingGroupID = bg.BuyingGroupID
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} customers!")
    conn.close()
    return df

def extract_products():
    conn = get_source_connection()
    logger.info("Extracting products...")
    query = """
        SELECT
            si.StockItemID,
            si.StockItemName,
            c.ColorName,
            si.UnitPrice,
            sg.StockGroupName
        FROM Warehouse.StockItems si
        LEFT JOIN Warehouse.Colors c
            ON si.ColorID = c.ColorID
        LEFT JOIN Warehouse.StockItemStockGroups sisg
            ON si.StockItemID = sisg.StockItemID
        LEFT JOIN Warehouse.StockGroups sg
            ON sisg.StockGroupID = sg.StockGroupID
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} products!")
    conn.close()
    return df

def extract_cities():
    conn = get_source_connection()
    logger.info("Extracting cities...")
    query = """
        SELECT
            ci.CityID,
            ci.CityName,
            sp.StateProvinceName,
            co.CountryName,
            sp.SalesTerritory
        FROM Application.Cities ci
        LEFT JOIN Application.StateProvinces sp
            ON ci.StateProvinceID = sp.StateProvinceID
        LEFT JOIN Application.Countries co
            ON sp.CountryID = co.CountryID
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} cities!")
    conn.close()
    return df

def extract_salespersons():
    conn = get_source_connection()
    logger.info("Extracting salespersons...")
    query = """
        SELECT
            PersonID,
            FullName,
            PreferredName,
            EmailAddress
        FROM Application.People
        WHERE IsSalesperson = 1
    """
    df = pd.read_sql(query, conn)
    logger.info(f"Extracted {len(df)} salespersons!")
    conn.close()
    return df