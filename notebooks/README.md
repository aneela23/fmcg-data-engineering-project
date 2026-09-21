# Databricks Pipeline Notebooks

This directory contains the Databricks notebooks used to build the FMCG data engineering pipeline following a Medallion Architecture.

## Notebook Structure

### 1. Setup
- `setup_catalogs.py` – Creates the required Unity Catalog schemas and project setup.
- `dim_date_table_creation.py` – Builds the date dimension used by the Gold analytics layer.

### 2. Dimension Data Processing
- `1_customer_data_processing.py` – Processes and standardizes customer data through Bronze, Silver, and Gold layers.
- `2_products_data_processing.py` – Cleans and transforms product data and integrates it into the Gold product dimension.
- `3_pricing_data_processing.py` – Processes pricing data and aligns child-company pricing with the consolidated Gold model.

### 3. Fact Data Processing
- `1_full_load_fact.py` – Performs the historical/full load of order data.
- `2_incremental_load_fact.py` – Processes new order files incrementally and updates the consolidated Gold fact table.

### Utilities
- `utilities.py` – Stores shared schema configuration used across the Databricks notebooks.

## Processing Flow

S3 → Bronze → Silver → Gold → Consolidated Gold → Analytics Dashboard

The production workflow is orchestrated using Databricks Workflows with dependency-based execution for customer, product, pricing, and incremental fact processing.
