# Databricks Pipeline Notebooks

This directory contains the Databricks notebooks used to build the **Retail Acquisition Data Integration Platform** using a Medallion Architecture.

The implementation is located in the [`consolidated_pipeline/`](consolidated_pipeline/) directory.

## Notebook Structure

### 1. Setup
- `setup_catalogs.py` – Creates the Unity Catalog schemas required for the pipeline.
- `dim_date_table_creation.py` – Builds the date dimension used by the Gold analytics layer.

### 2. Dimension Data Processing
- `1_customer_data_processing.py` – Cleans and standardizes customer data through Bronze, Silver, and Gold.
- `2_products_data_processing.py` – Processes product data and integrates it into the Gold product dimension.
- `3_pricing_data_processing.py` – Processes pricing data and aligns it with the consolidated Gold model.

### 3. Fact Data Processing
- `1_full_load_fact.py` – Performs the historical/full load of order data.
- `2_incremental_load_fact.py` – Processes newly arriving order files and incrementally updates the consolidated Gold fact table.

### 4. Analytics
- `create_enriched_sales_view.sql` – Creates the enriched Gold-layer sales view used by the **Retail Sales 360 Dashboard**.

### Utilities
- `utilities.py` – Contains shared schema configuration used across the Databricks notebooks.

## Processing Flow

**AWS S3 → Bronze → Silver → Gold → Consolidated Gold → Analytics**

The pipeline is orchestrated using **Databricks Workflows**, with dependency-based execution for customer, product, pricing, and incremental fact processing.
