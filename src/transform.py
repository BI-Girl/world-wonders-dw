import pandas as pd
from src.utils import setup_logger

logger = setup_logger(__name__)

def transform_customers(df):
    logger.info("Transforming customers...")
    df = df.drop_duplicates(subset=["CustomerID"])
    df.columns = ["customer_id", "customer_name",
                  "category", "buying_group", "credit_limit"]
    df["credit_limit"] = df["credit_limit"].fillna(0)
    df["customer_key"] = range(1, len(df) + 1)
    logger.info(f"Transformed {len(df)} customers!")
    return df

def transform_products(df):
    logger.info("Transforming products...")
    df = df.drop_duplicates(subset=["StockItemID"])
    df.columns = ["stock_item_id", "product_name",
                  "color", "unit_price", "stock_group"]
    df["color"] = df["color"].fillna("Unknown")
    df["stock_group"] = df["stock_group"].fillna("Unknown")
    df["product_key"] = range(1, len(df) + 1)
    logger.info(f"Transformed {len(df)} products!")
    return df

def transform_cities(df):
    logger.info("Transforming cities...")
    df = df.drop_duplicates(subset=["CityID"])
    df.columns = ["city_id", "city_name",
                  "state_province", "country", "sales_territory"]
    df["city_key"] = range(1, len(df) + 1)
    logger.info(f"Transformed {len(df)} cities!")
    return df

def transform_salespersons(df):
    logger.info("Transforming salespersons...")
    df = df.drop_duplicates(subset=["PersonID"])
    df.columns = ["person_id", "full_name",
                  "preferred_name", "email"]
    df["salesperson_key"] = range(1, len(df) + 1)
    logger.info(f"Transformed {len(df)} salespersons!")
    return df

def transform_date(df):
    logger.info("Building date dimension...")
    dates = pd.date_range(
        start=df["InvoiceDate"].min(),
        end=df["InvoiceDate"].max()
    )
    dim_date = pd.DataFrame({
        "date_key": dates.strftime("%Y%m%d").astype(int),
        "full_date": dates,
        "day_of_week": dates.dayofweek,
        "day_name": dates.strftime("%A"),
        "month": dates.month,
        "month_name": dates.strftime("%B"),
        "quarter": dates.quarter,
        "year": dates.year,
        "is_weekend": dates.dayofweek.isin([5, 6]).astype(int)
    })
    logger.info(f"Built {len(dim_date)} date records!")
    return dim_date

def transform_sales(df, dim_customer, dim_product, dim_salesperson):
    logger.info("Transforming sales with key lookups...")
    
    df["date_key"] = pd.to_datetime(
        df["InvoiceDate"]).dt.strftime("%Y%m%d").astype(int)
    
    df = df.merge(
        dim_customer[["customer_id", "customer_key"]],
        left_on="CustomerID", right_on="customer_id", how="left"
    )
    df = df.merge(
        dim_product[["stock_item_id", "product_key"]],
        left_on="StockItemID", right_on="stock_item_id", how="left"
    )
    df = df.merge(
        dim_salesperson[["person_id", "salesperson_key"]],
        left_on="SalespersonPersonID", right_on="person_id", how="left"
    )

    fact = df[[
        "InvoiceLineID", "InvoiceID",
        "customer_key", "product_key",
        "salesperson_key", "date_key",
        "Quantity", "UnitPrice",
        "TaxAmount", "LineProfit", "ExtendedPrice"
    ]].rename(columns={
        "InvoiceLineID": "invoice_line_id",
        "InvoiceID": "invoice_id",
        "Quantity": "quantity",
        "UnitPrice": "unit_price",
        "TaxAmount": "tax_amount",
        "LineProfit": "line_profit",
        "ExtendedPrice": "extended_price"
    })

    logger.info(f"Transformed {len(fact)} sales rows!")
    return fact