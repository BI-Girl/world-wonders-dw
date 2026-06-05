from src.utils import setup_logger
from src.extract import (extract_sales, extract_customers,
                         extract_products, extract_cities,
                         extract_salespersons)
from src.transform import (transform_customers, transform_products,
                           transform_cities, transform_salespersons,
                           transform_date, transform_sales)
from src.load import (load_customers, load_products, load_cities,
                      load_salespersons, load_dates, load_sales)
from src.create_dw import run_create_dw

logger = setup_logger(__name__)

def run_pipeline():
    logger.info("========== Pipeline started ==========")

    logger.info("--- Setting up DW ---")
    run_create_dw()

    logger.info("--- Extracting ---")
    raw_sales = extract_sales()
    raw_customers = extract_customers()
    raw_products = extract_products()
    raw_cities = extract_cities()
    raw_salespersons = extract_salespersons()

    logger.info("--- Transforming ---")
    dim_customer = transform_customers(raw_customers)
    dim_product = transform_products(raw_products)
    dim_city = transform_cities(raw_cities)
    dim_salesperson = transform_salespersons(raw_salespersons)
    dim_date = transform_date(raw_sales)
    fact_sales = transform_sales(raw_sales, dim_customer, dim_product, dim_salesperson)

    logger.info("--- Loading ---")
    load_customers(dim_customer)
    load_products(dim_product)
    load_cities(dim_city)
    load_salespersons(dim_salesperson)
    load_dates(dim_date)
    load_sales(fact_sales)

    logger.info("========== Pipeline complete! ==========")

if __name__ == "__main__":
    run_pipeline()