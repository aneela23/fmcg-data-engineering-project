# FMCG Data Engineering Platform

An end-to-end data engineering project that integrates FMCG sales data from a parent company and an acquired child company.

The project demonstrates data ingestion, data quality, transformation, dimensional modeling, incremental processing, data consolidation, and analytics using modern data engineering technologies.

---

## 📌 Project Overview

This project simulates an FMCG (Fast-Moving Consumer Goods) business scenario where a parent company acquires a child company.

The parent company already has an established analytical data platform, while the child company has data coming from separate source files with different structures and data-quality issues.

The goal is to build a scalable data pipeline that:

- Ingests child-company source data
- Preserves raw data
- Cleans and standardizes data
- Transforms data into business-ready datasets
- Aligns child-company data with the parent-company data model
- Consolidates parent and child data
- Supports analytical and BI workloads

---

## 🎯 Project Objectives

- Build an end-to-end data engineering pipeline
- Implement a Medallion Architecture
- Practice PySpark and SQL transformations
- Implement data-quality rules
- Work with fact and dimension tables
- Implement incremental data processing
- Consolidate data from parent and child companies
- Create analytics-ready datasets
- Build a foundation for BI reporting
- Practice Databricks concepts relevant to the Databricks Data Engineer certification

---

## 🏗️ Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL | Relational source database |
| DBeaver | Database development and ER diagrams |
| Python | Data engineering and utility logic |
| SQL | Data modeling, validation and analytics |
| AWS S3 | Data lake / file storage |
| Databricks | Data engineering platform |
| PySpark | Large-scale data transformation |
| Delta Lake | Transactional data storage |
| Airflow / Databricks Workflows | Pipeline orchestration |
| GitHub | Source control and documentation |
| Power BI | Analytics and visualization |

---

## 🏛️ Architecture

The project follows a Medallion Architecture for the child-company data pipeline.

The parent company is represented by an existing analytical data model, while the acquired child company goes through the complete Bronze → Silver → Gold pipeline before being consolidated with the parent-company data.

```text
                    PARENT COMPANY
                    PostgreSQL
                         |
                         v
                  Parent Data Model
                    /    |     \
                   /     |      \
                  v      v       v
             Customers Products Gross Price
                   \      |      /
                    \     |     /
                     v    v    v
                   Fact Orders
                         |
                         v
                  Parent Gold Data
                         |
                         v
              +----------------------+
              |   CONSOLIDATED GOLD  |
              |  Parent + Child Data |
              +----------------------+
                         ^
                         |
                    CHILD COMPANY
                    Sports Bar
                         |
                         v
                        S3
                         |
                         v
                      BRONZE
                    Raw Data
                         |
                         v
                      SILVER
             Cleaning & Standardization
                         |
                         v
                       GOLD
                Business-Ready Data
                         |
                         v
                Child Gold Data
                         |
                         v
              Parent + Child Merge
```

---

## 📊 Parent Company Data Model

The parent company data represents the existing analytical data model used as the target structure for integrating the acquired child company's data.

### PostgreSQL Source Model

The parent-company data was initially loaded into PostgreSQL using DBeaver.

```text
parent_company
│
├── dim_customers
├── dim_products
├── dim_gross_price
└── fact_orders
```



### Source Data Validation

The parent-company source tables were validated in PostgreSQL before being used in the Databricks environment.

| Table | Records | Primary Key |
|---|---:|---|
| `dim_customers` | 18 | `customer_code` |
| `dim_products` | 397 | `product_code` |
| `dim_gross_price` | 794 | `product_code`, `year` |
| `fact_orders` | 93,055 | `date`, `product_code`, `customer_code` |

Foreign-key relationships were validated between `fact_orders` and the customer and product dimensions.

### Databricks Gold Model

The existing parent-company analytical data was loaded into the Databricks Gold layer to represent the established enterprise data platform.

```text
fmcg.gold
│
├── dim_customers
├── dim_products
├── dim_gross_price
├── dim_date
└── fact_orders
```

The `dim_date` dimension is maintained in the Databricks analytical layer to support time-based reporting and analysis.

---

## 🔄 Child Company Data Pipeline

The acquired child-company (Sports Bar) data is stored in AWS S3 and processed through the Databricks Medallion Architecture.

### Bronze Layer

Raw customer data is ingested from AWS S3 into Delta Lake without business transformations.

Implemented:

- Connected Databricks to the Sports Bar data stored in AWS S3
- Loaded raw customer data into `fmcg.bronze.customers`
- Preserved the source data for traceability
- Enabled Delta Change Data Feed (CDF)

### Silver Layer

The Bronze customer data is cleaned and standardized using PySpark before integration with the parent-company data model.

Implemented:

- Removed duplicate customer records
- Trimmed whitespace from customer names
- Standardized customer-name capitalization
- Cleaned and standardized city values
- Handled missing city information using business mappings
- Converted customer identifiers to the required data type
- Added `market`, `platform`, and `channel` attributes
- Created a standardized customer field for integration

The processed customer data is stored in:

`fmcg.silver.customers`

The next stage transforms the standardized Silver data into the Gold model and consolidates it with the parent-company customer dimension.
