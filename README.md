# Retail Acquisition Data Integration Platform

An end-to-end data engineering project that integrates sales data from a parent retail company and an acquired company using **AWS S3, Databricks, PySpark, Delta Lake, PostgreSQL, and SQL**.

The project demonstrates a post-acquisition data integration scenario covering **data ingestion, Medallion Architecture, data quality, dimensional modeling, historical and incremental processing, workflow orchestration, and analytics**.

---

## 📌 Project Overview

This project simulates a business acquisition where an established parent company needs to integrate data from a newly acquired company operating with a separate data platform.

The parent company already has an analytical data model, while the acquired company provides customer, product, pricing, and order data through separate source files with different schemas and data-quality issues.

The pipeline standardizes the acquired-company data and integrates it with the existing parent-company model to create a **unified analytics-ready Gold layer**.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| PostgreSQL / DBeaver | Parent-company source and data validation |
| AWS S3 | Acquired-company source and landing/processed zones |
| Databricks | Lakehouse data engineering and analytics |
| PySpark | Data cleansing and transformations |
| SQL | Data validation, modeling, and analytics |
| Delta Lake | Transactional storage and MERGE operations |
| Unity Catalog | Lakehouse data organization |
| Databricks Workflows | Pipeline orchestration |
| Databricks AI/BI | Analytics and visualization |
| GitHub | Version control and documentation |

---

## 🏗️ Architecture

The parent-company data represents an existing analytical platform, while acquired-company data is ingested from **AWS S3** and processed through a **Bronze → Silver → Gold Medallion Architecture**.

Both data sources are standardized and integrated into a consolidated Gold layer for downstream analytics.

```text
Parent Company                         Acquired Company
   PostgreSQL                               AWS S3
       │                                       │
       ▼                                       ▼
Databricks Gold                            Bronze
       │                                       │
       │                                       ▼
       │                                    Silver
       │                                       │
       │                                       ▼
       │                                     Gold
       │                                       │
       └───────────────┬───────────────────────┘
                       ▼
                Consolidated Gold
                       │
                       ▼
                    Analytics
```

📊 [View End-to-End Architecture](architecture/images/end-to-end-data-architecture.png)  
📂 [View Architecture Documentation & Diagrams](architecture/)

---

## 📊 Data Model

The consolidated Gold layer follows a dimensional model containing:

```text
fmcg.gold
│
├── dim_customers
├── dim_products
├── dim_gross_price
├── dim_date
└── fact_orders
```

The parent-company source data was validated in PostgreSQL for **primary-key uniqueness, null constraints, and fact-to-dimension relationships** before integration.

📊 [View Parent Company Data Model](architecture/images/parent-company-data-model.png)

---

## 🥉🥈🥇 Medallion Data Pipeline

### Bronze

Raw customer, product, pricing, and order data is ingested from AWS S3 into Delta tables while preserving source-level data for traceability and reprocessing.

### Silver

PySpark transformations handle:

- Deduplication and missing values
- Data-type and schema standardization
- Customer and location cleansing
- Product, category, variant, and division standardization
- Pricing and order transformations
- Alignment with the parent-company data model

### Gold

Business-ready dimensions and facts are created and integrated with the parent-company model using **Delta Lake MERGE operations**.

📂 [View Databricks Pipeline Notebooks](notebooks/)  
📄 [View Data Quality Rules](data-quality/data-quality-rules.md)

---

## ⚡ Historical & Incremental Processing

The order pipeline supports both an initial **historical load** and incremental processing of newly arriving order files.

For incremental processing, a staging layer isolates the current batch so only newly arrived data is transformed. Bronze maintains the complete raw history, while successfully processed source files are moved from the S3 `landing` location to `processed` to prevent duplicate processing.

```text
New Order File
      │
      ▼
  S3 Landing
      │
      ├──────► Bronze (Raw History)
      │
      ▼
   Staging
      │
      ▼
    Silver
      │
      ▼
 Child Gold
      │
      ▼
Consolidated Gold
```

The incremental pipeline uses **Delta Lake MERGE** operations to update the appropriate Gold datasets without reprocessing the complete historical dataset.

📊 [View Incremental Processing Architecture](architecture/images/incremental-processing-architecture.png)  
📂 [View Fact Processing Notebooks](notebooks/consolidated_pipeline/3_fact_data_processing/)

---

## ⚙️ Databricks Workflow Orchestration

The acquired-company pipeline is orchestrated using **Databricks Workflows** with dependency-based execution:

**Customers → Products → Gross Price → Incremental Fact Orders**

The workflow automates dimension processing followed by incremental fact processing and updates the consolidated Gold model when new order data arrives.

📷 [View Successful Workflow Execution](screenshots/databricks-workflow-success.png)

---

## 📥 Parent Company Incremental Load

New parent-company order data is incrementally loaded into the consolidated Gold fact table using Databricks **`COPY INTO`**.

The incremental load processed **4,485 new records with zero corrupt files**, bringing the consolidated `fact_orders` table to **101,212 records**.

This demonstrates an additional incremental ingestion pattern alongside the Delta Lake MERGE-based acquired-company pipeline.

---

## 📈 Analytics Layer

An analytics-ready Gold view, **`fmcg.gold.vw_fact_orders_enriched`**, combines consolidated order data with customer, product, pricing, and date dimensions.

The view provides the reporting layer for the **Retail Sales 360 Dashboard**, built using Databricks AI/BI to analyze:

- Revenue and quantity sold
- Customer performance
- Product and variant performance
- Revenue by sales channel
- Monthly revenue trends
- Product price vs. sales volume

📄 [View Analytics SQL](notebooks/consolidated_pipeline/4_analytics/create_enriched_sales_view.sql)  
📊 [View Retail Sales 360 Dashboard](screenshots/retail-sales-360-dashboard.png)

---

## 📁 Repository Structure

```text
retail-acquisition-data-integration/
│
├── architecture/
│   ├── architecture.md
│   └── images/
│       ├── parent-company-data-model.png
│       ├── end-to-end-data-architecture.png
│       └── incremental-processing-architecture.png
│
├── data-quality/
│   └── data-quality-rules.md
│
├── notebooks/
│   ├── README.md
│   └── consolidated_pipeline/
│       ├── 1_setup/
│       ├── 2_dimension_data_processing/
│       ├── 3_fact_data_processing/
│       ├── 4_analytics/
│       └── utilities.py
│
├── screenshots/
│   ├── databricks-workflow-success.png
│   └── retail-sales-360-dashboard.png
│
└── README.md
```

---

## 🔑 Key Engineering Concepts

**AWS S3 • Databricks • PySpark • SQL • Delta Lake • Unity Catalog • Medallion Architecture • ETL/ELT • Dimensional Modeling • Data Quality • Historical & Incremental Processing • Delta MERGE • COPY INTO • Databricks Workflows • Analytics**
