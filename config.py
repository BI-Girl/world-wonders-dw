import os
from dotenv import load_dotenv

load_dotenv()

# Source database
SOURCE_SERVER = "172.20.80.1"
SOURCE_DB = "WideWorldImporters"

# Data warehouse database
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Paths
LOGS_PATH = "logs/"

# DW schema
DW_SCHEMA = "dw"

# Date range for extraction
START_DATE = "2013-01-01"
END_DATE = "2016-12-31"