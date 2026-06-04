import os
from dotenv import load_dotenv

load_dotenv()

# Source database
SOURCE_SERVER = "localhost"
SOURCE_DB = "WideWorldImporters"

# Data warehouse database
DW_SERVER = "localhost"
DW_DB = "WorldWondersDW"

# Paths
LOGS_PATH = "logs/"

# DW schema
DW_SCHEMA = "dw"

# Date range for extraction
START_DATE = "2013-01-01"
END_DATE = "2016-12-31"